# backend/tests/test_rag_e2e.py
"""End-to-end RAG pipeline: ingest -> chunk -> FTS -> retrieve -> generate -> persist.

Synthetic lesson + injected fetcher; no network, no HF model download.
"""
import json
import sqlite3
import pytest

from scripts.ingest_transcripts import ingest_lesson
from app.services import groq_service as gs
from app.services import retrieval_service
from app.routers import practice_router


@pytest.fixture()
def con(tmp_path):
    c = sqlite3.connect(tmp_path / "e2e.sqlite")
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE transcript_chunks (
        chunk_id TEXT PRIMARY KEY, lesson_id TEXT, course_id TEXT, competency_id TEXT,
        topic TEXT, start_seconds INTEGER, end_seconds INTEGER, timestamp_label TEXT,
        text_content TEXT, summary TEXT, provenance TEXT)""")
    c.execute("""CREATE VIRTUAL TABLE transcript_fts USING fts5(
        chunk_id UNINDEXED, text_content, topic, tokenize='unicode61')""")
    c.execute("""CREATE TABLE raw_transcripts (
        lesson_id TEXT PRIMARY KEY, transcript_text TEXT, language TEXT,
        source TEXT, fetched_at TEXT, status TEXT)""")
    c.execute("""CREATE TABLE chunk_embeddings (
        chunk_id TEXT PRIMARY KEY, embedding BLOB, model_name TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE curated_lessons (
        lesson_id TEXT PRIMARY KEY, playlist_id TEXT, sequence_no INTEGER, title TEXT,
        youtube_video_id TEXT, youtube_url TEXT, duration_minutes INTEGER,
        competency_id TEXT, has_transcript INTEGER)""")
    c.execute("""CREATE TABLE curated_playlists (playlist_id TEXT PRIMARY KEY, title TEXT)""")
    c.execute("""CREATE TABLE practice_quizzes (
        quiz_id TEXT PRIMARY KEY, lesson_id TEXT, course_id TEXT, competency_id TEXT,
        title TEXT, topic TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE practice_questions (
        question_id TEXT PRIMARY KEY, quiz_id TEXT, lesson_id TEXT, competency_id TEXT,
        question_text TEXT, options_json TEXT, correct_option TEXT, explanation TEXT,
        chunk_id TEXT, timestamp_label TEXT, difficulty TEXT, is_approved INTEGER,
        review_status TEXT)""")
    yield c
    c.close()


LONG_TEXT = " ".join([
    "Stratified sampling divides the population into non-overlapping homogeneous strata.",
    "Samples are drawn independently from each stratum in the sampling frame.",
    "Proportional allocation assigns sample sizes in proportion to stratum population sizes.",
    "Sampling weights equal the inverse of the inclusion probability of each unit.",
    "Frame undercoverage omits eligible population units from the operational list.",
] * 20)  # long enough to yield >= 5 overlapping chunks


def test_full_pipeline(con, monkeypatch):
    # 1. INGEST (fetcher injected; no network)
    lesson = {"lesson_id": "e2e-lesson-1", "title": "Sampling Fundamentals",
              "competency_id": "COMP-SAMPLING", "course_id": "CRS-101",
              "youtube_video_id": "vid", "duration_minutes": 30}
    result = ingest_lesson(
        con, lesson,
        fetcher=lambda l: {"text": LONG_TEXT, "language": "en",
                           "source": "YOUTUBE_MANUAL", "start": 0, "end": 1800},
        embed=False,
    )
    assert result["status"] == "INGESTED"
    assert result["chunks_written"] >= 5

    # 2. RETRIEVE (vector leg off in this test; FTS5 live)
    monkeypatch.setattr(retrieval_service, "_vector_ids_and_matrix",
                        lambda con: (None, None))
    hits = retrieval_service.retrieve(
        "What is proportional allocation?", lesson_id="e2e-lesson-1", con=con)
    assert hits, "retrieval returned nothing"
    assert any("Proportional allocation" in h["text_content"] for h in hits)

    # 3. GENERATE QUIZ (deterministic mocked LLM)
    top = hits[0]
    good_q = {
        "question_text": "How does proportional allocation assign stratum sample sizes?",
        "options": [
            {"text": "In proportion to stratum population sizes"},
            {"text": "Equally to all strata"},
            {"text": "By alphabetical order"},
            {"text": "Randomly regardless of size"},
        ],
        "correct_index": 0,
        "explanation": "Proportional allocation assigns sample sizes in proportion to stratum population sizes.",
        "difficulty": "MEDIUM",
        "timestamp_label": top["timestamp_label"],
        "chunk_id": top["chunk_id"],
    }
    monkeypatch.setattr(gs, "_llm_generate",
                        lambda *a, **kw: json.dumps({"questions": [good_q] * 3}))

    class OfflineEmb:
        @staticmethod
        def embed_texts(texts):
            return None

    monkeypatch.setattr(gs, "_embedding_probe", OfflineEmb)
    questions = gs.generate_quiz_questions(
        {"lesson_id": "e2e-lesson-1", "title": "Sampling Fundamentals",
         "competency_id": "COMP-SAMPLING"},
        hits, num_questions=5,
    )
    assert questions and len(questions) == 3
    assert questions[0]["chunk_id"] == top["chunk_id"]

    # 4. PERSIST + SERVE
    # Preflight ruling: _persist_ai_quiz reads lesson['title'] for the quiz title
    # # f-string, so the persist call must carry it alongside lesson_id/competency_id.
    quiz_id = practice_router._persist_ai_quiz(
        con, {"lesson_id": "e2e-lesson-1", "competency_id": "COMP-SAMPLING",
              "title": "Sampling Fundamentals"},
        questions)
    served = con.execute(
        "SELECT COUNT(*) c FROM practice_questions WHERE quiz_id = ?", (quiz_id,)
    ).fetchone()
    assert served["c"] == 3

    # 5. SCOPE SANITY: scoped retrieval never leaks other lessons
    scoped = retrieval_service.retrieve(
        "sampling weights", lesson_id="e2e-lesson-1", con=con)
    assert scoped and all(h["lesson_id"] == "e2e-lesson-1" for h in scoped)
