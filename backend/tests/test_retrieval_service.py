# backend/tests/test_retrieval_service.py
import sqlite3
import pytest
from app.services import embedding_service, reranker_service, retrieval_service
from app.services.retrieval_service import rrf_fuse, rebuild_fts, retrieve


@pytest.fixture()
def con(tmp_path, monkeypatch):
    # Hermeticity: never load/download the real embedding or reranker models in tests.
    monkeypatch.setattr(embedding_service, "_model", None)
    monkeypatch.setattr(embedding_service, "_load_failed", True)
    monkeypatch.setattr(reranker_service, "_model", None)
    monkeypatch.setattr(reranker_service, "_load_failed", True)
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


def test_retrieve_uses_reranker_when_available(con, monkeypatch):
    from app.services import reranker_service

    class FakeModel:
        def predict(self, pairs):
            return [9.0 if "weights" in t else 1.0 for _, t in pairs]

    monkeypatch.setattr(reranker_service, "_model", FakeModel())
    monkeypatch.setattr(reranker_service, "_load_failed", False)
    # Force FTS5 leg to return a deterministic order where the weights chunk ranks SECOND
    scrambled = [
        {"chunk_id": "CHK-T-001", "text_content": "Stratified sampling divides population.",
         "lesson_id": "lesson-1", "start_seconds": 0, "end_seconds": 90,
         "lesson_title": "L", "playlist_title": "P", "timestamp_label": "00:00",
         "topic": "t", "course_id": "C", "competency_id": "K", "summary": "", "end_offset": 0},
        {"chunk_id": "CHK-T-002", "text_content": "Sampling weights are inverse selection probability.",
         "lesson_id": "lesson-2", "start_seconds": 100, "end_seconds": 190,
         "lesson_title": "L", "playlist_title": "P", "timestamp_label": "00:00",
         "topic": "t", "course_id": "C", "competency_id": "K", "summary": "", "end_offset": 0},
    ]
    monkeypatch.setattr(retrieval_service, "fts5_search",
                        lambda con, q, *a, **kw: scrambled)
    monkeypatch.setattr(retrieval_service, "_vector_ids_and_matrix", lambda con: (None, None))
    hits = retrieve("what are sampling weights", con=con)
    assert hits[0]["chunk_id"] == "CHK-T-002"


def test_fts5_search_matches_hyphenated_terms():
    # FTS5 treats a bare hyphen as the NOT operator ("hot-deck" -> "hot NOT deck"),
    # which raises a syntax error the old code swallowed into [] silently.
    # Quoting terms makes "hot-deck" a phrase query that matches the chunk text.
    from app.services.retrieval_service import fts5_search

    con_fixture = sqlite3.connect(":memory:")
    con_fixture.row_factory = sqlite3.Row
    con_fixture.execute("""CREATE TABLE transcript_chunks (
        chunk_id TEXT PRIMARY KEY, lesson_id TEXT, course_id TEXT, competency_id TEXT,
        topic TEXT, start_seconds INTEGER, end_seconds INTEGER, timestamp_label TEXT,
        text_content TEXT, summary TEXT, provenance TEXT)""")
    con_fixture.execute("""CREATE VIRTUAL TABLE transcript_fts USING fts5(
        chunk_id UNINDEXED, text_content, topic, tokenize='unicode61')""")
    con_fixture.execute("""CREATE TABLE curated_lessons (
        lesson_id TEXT PRIMARY KEY, playlist_id TEXT, sequence_no INTEGER, title TEXT,
        youtube_video_id TEXT, youtube_url TEXT, duration_minutes INTEGER,
        competency_id TEXT, has_transcript INTEGER)""")
    con_fixture.execute("""CREATE TABLE curated_playlists (playlist_id TEXT PRIMARY KEY, title TEXT)""")
    con_fixture.execute("""CREATE TABLE chunk_embeddings (
        chunk_id TEXT PRIMARY KEY, embedding BLOB, model_name TEXT, created_at TEXT)""")
    con_fixture.execute(
        "INSERT INTO transcript_chunks VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        ("CHK-T-005", "lesson-5", "CRS-5", "COMP-5", "topic", 400, 490, "00:00",
         "Donor hot-deck imputation preserves empirical distributions for item non-response.", "", "AUTO_CHUNK"),
    )
    rebuild_fts(con_fixture)
    hits = fts5_search(con_fixture, "How does donor hot-deck imputation preserve distributions?")
    assert any(h["chunk_id"] == "CHK-T-005" for h in hits)
    con_fixture.close()
