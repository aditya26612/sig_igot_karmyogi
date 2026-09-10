# backend/tests/test_retrieval_service.py
import sqlite3
import pytest
from app.services import embedding_service, retrieval_service
from app.services.retrieval_service import rrf_fuse, rebuild_fts, retrieve


@pytest.fixture()
def con(tmp_path, monkeypatch):
    # Hermeticity: never load/download the real embedding model in tests.
    monkeypatch.setattr(embedding_service, "_model", None)
    monkeypatch.setattr(embedding_service, "_load_failed", True)
    c = sqlite3.connect(tmp_path / "r.sqlite")
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE transcript_chunks (
        chunk_id TEXT PRIMARY KEY, lesson_id TEXT, course_id TEXT, competency_id TEXT,
        topic TEXT, start_seconds INTEGER, end_seconds INTEGER, timestamp_label TEXT,
        text_content TEXT, summary TEXT, provenance TEXT)""")
    c.execute("""CREATE VIRTUAL TABLE transcript_fts USING fts5(
        chunk_id UNINDEXED, text_content, topic, tokenize='unicode61')""")
    c.execute("""CREATE TABLE curated_lessons (
        lesson_id TEXT PRIMARY KEY, playlist_id TEXT, sequence_no INTEGER, title TEXT,
        youtube_video_id TEXT, youtube_url TEXT, duration_minutes INTEGER,
        competency_id TEXT, has_transcript INTEGER)""")
    c.execute("""CREATE TABLE curated_playlists (playlist_id TEXT PRIMARY KEY, title TEXT)""")
    c.execute("""CREATE TABLE chunk_embeddings (
        chunk_id TEXT PRIMARY KEY, embedding BLOB, model_name TEXT, created_at TEXT)""")
    for i, (cid, txt) in enumerate([
        ("CHK-T-001", "Stratified sampling divides the population into homogeneous strata and samples from every stratum."),
        ("CHK-T-002", "Sampling weights are the inverse of the selection probability of each unit."),
        ("CHK-T-003", "SQL LEFT JOIN retains all survey records and exposes unmatched tax register entries."),
        ("CHK-T-004", "The Central Limit Theorem makes sample means approximately normal for large n."),
    ]):
        c.execute(
            "INSERT INTO transcript_chunks VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (cid, f"lesson-{i+1}", f"CRS-{i+1}", f"COMP-{i}", "topic", i * 100,
             i * 100 + 90, "00:00", txt, "", "AUTO_CHUNK"),
        )
        c.execute(
            "INSERT OR IGNORE INTO curated_lessons VALUES (?,?,?,?,?,?,?,?,?)",
            (f"lesson-{i+1}", f"PL-{i+1}", 1, f"Lesson {i+1}", "vid", "url", 30, f"COMP-{i}", 1),
        )
        c.execute(
            "INSERT OR IGNORE INTO curated_playlists VALUES (?,?)",
            (f"PL-{i+1}", f"Playlist {i+1}"),
        )
    rebuild_fts(c)
    yield c
    c.close()


def test_rrf_fuse_prefers_both_legs():
    lex = ["A", "B", "C"]
    sem = ["B", "D", "A"]
    fused = rrf_fuse(lex, sem, k=60)
    assert fused[0] in ("A", "B")
    assert set(fused) == {"A", "B", "C", "D"}


def test_fts5_search_ranks_relevant_chunk_first(con):
    hits = retrieval_service.fts5_search(con, "stratified strata")
    assert hits and hits[0]["chunk_id"] == "CHK-T-001"


def test_retrieve_without_embeddings_is_fts_only(con, monkeypatch):
    monkeypatch.setattr(retrieval_service, "_vector_ids_and_matrix", lambda con: (None, None))
    hits = retrieve("What are sampling weights?", con=con)
    assert hits and hits[0]["chunk_id"] == "CHK-T-002"


def test_retrieve_respects_lesson_scope(con, monkeypatch):
    monkeypatch.setattr(retrieval_service, "_vector_ids_and_matrix", lambda con: (None, None))
    hits = retrieve("sampling", lesson_id="lesson-1", con=con)
    assert hits and all(h["lesson_id"] == "lesson-1" for h in hits)


def test_retrieve_empty_on_no_match(con, monkeypatch):
    monkeypatch.setattr(retrieval_service, "_vector_ids_and_matrix", lambda con: (None, None))
    assert retrieve("quantum thermodynamics of quarks", con=con) == []
