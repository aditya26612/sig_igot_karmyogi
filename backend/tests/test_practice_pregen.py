# backend/tests/test_practice_pregen.py
"""Task 11: background quiz pre-generation (fire-and-forget prewarm).

Hermeticity strategy (documented per the task-11 context):

- ``practice_router.get_db_connection`` is monkeypatched to open a fresh
  connection to a throwaway ``tmp_path`` SQLite DB seeded with the tables
  the prewarm job touches (curated_lessons, curated_playlists,
  transcript_chunks, transcript_fts, practice_quizzes,
  practice_questions). The background job therefore never opens the real
  demo.sqlite and its early-exit cache check (existing ``QUIZ-AI-%`` row)
  starts from an empty table.
- ``embedding_service`` / ``reranker_service`` are forced offline with the
  established ``_model=None, _load_failed=True`` pattern (see
  ``tests/test_module6.py::_offline_rag_models`` and the fixture in
  ``tests/test_groq_service_rag.py``). This is required because the prewarm
  job calls ``retrieval_service.retrieve`` BEFORE the mocked generator;
  without the guard the background thread would load the real 458MB
  embedding model and, on FTS hits, the 2.2GB reranker. Offline, retrieval
  degrades to the FTS5 lexical leg over the fixture DB (whose FTS index is
  populated below), so the relevance-ranked context path is still exercised.
- ``groq_service.generate_quiz_questions`` is monkeypatched to a counting
  stub, so no Groq/LLM network call is made.
- The lesson id is unique to this file: other tests hit the lesson-detail
  endpoint (which now triggers prewarm) and their daemon threads share the
  module-level ``_prewarm_inflight`` set; a unique id eliminates any
  cross-test single-flight collision.
"""
import sqlite3
import threading
import time

import pytest

from app.routers import practice_router
from app.services import embedding_service, reranker_service, retrieval_service

LESSON_ID = "pregen-hermetic-lesson"
LESSON_TITLE = "Stratified Sampling Basics"


@pytest.fixture()
def hermetic_prewarm_db(tmp_path, monkeypatch):
    """Throwaway DB + offline RAG models + patched practice_router DB factory."""
    db_path = tmp_path / "pregen.sqlite"

    # Hermeticity: no local embedding/reranker model loads from the
    # background prewarm thread (retrieval keeps the FTS5 lexical leg only).
    monkeypatch.setattr(embedding_service, "_model", None)
    monkeypatch.setattr(embedding_service, "_load_failed", True)
    monkeypatch.setattr(reranker_service, "_model", None)
    monkeypatch.setattr(reranker_service, "_load_failed", True)

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    # Schemas mirror demo.sqlite for the tables the prewarm job reads/writes.
    con.execute("""CREATE TABLE curated_lessons (
        lesson_id TEXT PRIMARY KEY, playlist_id TEXT, sequence_no INTEGER,
        title TEXT, youtube_video_id TEXT, youtube_url TEXT,
        duration_minutes INTEGER, competency_id TEXT, has_transcript INTEGER)""")
    con.execute("CREATE TABLE curated_playlists (playlist_id TEXT PRIMARY KEY, title TEXT)")
    con.execute("""CREATE TABLE transcript_chunks (
        chunk_id TEXT PRIMARY KEY, lesson_id TEXT, course_id TEXT,
        competency_id TEXT, topic TEXT, start_seconds INTEGER, end_seconds INTEGER,
        timestamp_label TEXT, text_content TEXT, summary TEXT, provenance TEXT)""")
    con.execute("""CREATE VIRTUAL TABLE transcript_fts USING fts5(
        chunk_id UNINDEXED, text_content, topic, tokenize='unicode61')""")
    con.execute("""CREATE TABLE practice_quizzes (
        quiz_id TEXT PRIMARY KEY, lesson_id TEXT, course_id TEXT,
        competency_id TEXT, title TEXT, topic TEXT, created_at TEXT)""")
    con.execute("""CREATE TABLE practice_questions (
        question_id TEXT PRIMARY KEY, quiz_id TEXT, lesson_id TEXT,
        competency_id TEXT, question_text TEXT, options_json TEXT,
        correct_option TEXT, explanation TEXT, chunk_id TEXT,
        timestamp_label TEXT, difficulty TEXT, is_approved INTEGER,
        review_status TEXT)""")

    con.execute("INSERT INTO curated_playlists VALUES ('PL-PREGEN', 'Prewarm Fixture Playlist')")
    con.execute(
        "INSERT INTO curated_lessons VALUES (?, 'PL-PREGEN', 1, ?, 'vid', 'url', 10, 'COMP-PREGEN', 1)",
        (LESSON_ID, LESSON_TITLE),
    )
    con.execute(
        """INSERT INTO transcript_chunks VALUES
        ('CHK-PREGEN-001', ?, 'CRS-PREGEN', 'COMP-PREGEN', 'Stratified sampling', 0, 120, '00:00',
         'Stratified sampling divides the population into homogeneous strata before drawing a sample.',
         NULL, 'SEED')""",
        (LESSON_ID,),
    )
    con.execute(
        """INSERT INTO transcript_chunks VALUES
        ('CHK-PREGEN-002', ?, 'CRS-PREGEN', 'COMP-PREGEN', 'Proportional allocation', 120, 240, '02:00',
         'Proportional allocation assigns sample sizes per stratum in proportion to stratum size.',
         NULL, 'SEED')""",
        (LESSON_ID,),
    )
    retrieval_service.rebuild_fts(con)
    con.commit()
    con.close()

    def _fake_get_db_connection():
        # Mirrors app.database.get_db_connection but on the fixture file, so
        # the prewarm job's con is a per-thread connection to tmp data.
        c = sqlite3.connect(db_path, check_same_thread=False)
        c.execute("PRAGMA foreign_keys = ON")
        c.row_factory = sqlite3.Row
        return c

    # The prewarm job must hit the fixture DB, never the real demo.sqlite.
    monkeypatch.setattr(practice_router, "get_db_connection", _fake_get_db_connection)
    yield db_path


def test_prewarm_single_flight_per_lesson(hermetic_prewarm_db, monkeypatch):
    calls = []
    lock = threading.Lock()

    def slow_gen(lesson, chunks, num_questions):
        with lock:
            calls.append(lesson["lesson_id"])
        time.sleep(0.3)
        return None

    monkeypatch.setattr(practice_router.groq_service, "generate_quiz_questions", slow_gen)
    practice_router._prewarm_inflight.clear()
    practice_router.prewarm_quiz_for_lesson(LESSON_ID)
    practice_router.prewarm_quiz_for_lesson(LESSON_ID)  # in-flight duplicate
    # Wait for the background job to drain (the brief used a flat 0.6s sleep;
    # polling the in-flight set for THIS lesson is the robust equivalent and
    # is immune to unrelated daemon prewarm threads from other tests).
    deadline = time.time() + 5.0
    while LESSON_ID in practice_router._prewarm_inflight and time.time() < deadline:
        time.sleep(0.05)
    assert calls.count(LESSON_ID) == 1
    # Idempotency: the in-flight guard must be released so a later retry can run.
    assert LESSON_ID not in practice_router._prewarm_inflight
    # Best-effort contract: the generator returned None -> nothing persisted.
    check = sqlite3.connect(hermetic_prewarm_db)
    try:
        persisted = check.execute(
            "SELECT COUNT(*) FROM practice_quizzes WHERE quiz_id LIKE 'QUIZ-AI-%'"
        ).fetchone()[0]
    finally:
        check.close()
    assert persisted == 0
