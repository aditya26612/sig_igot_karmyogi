# backend/tests/test_content_search.py
import sqlite3
import pytest
from app.routers import content_router
from app.services import retrieval_service


@pytest.fixture()
def con(tmp_path):
    c = sqlite3.connect(tmp_path / "c.sqlite")
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
    c.execute("""INSERT INTO transcript_chunks VALUES
        ('CHK-T-001','lesson-1','CRS-1','COMP-1','weights',100,200,'01:40',
         'Sampling weights are the inverse of selection probability.','s','SEED')""")
    c.execute("INSERT INTO curated_lessons VALUES ('lesson-1','PL',1,'L','v','u',30,'COMP-1',1)")
    c.execute("INSERT INTO curated_playlists VALUES ('PL','P')")
    retrieval_service.rebuild_fts(c)
    yield c
    c.close()


def test_search_chunks_fts5_first(con):
    results = content_router._search_chunks(con, "sampling weights")
    assert results and results[0]["chunk_id"] == "CHK-T-001"
    assert "matching_snippet" in results[0]
    assert results[0]["lesson_title"] == "L"


def test_search_chunks_falls_back_to_like(con, monkeypatch):
    def broken_fts(con, q, *a, **kw):
        raise sqlite3.OperationalError("fts5 exploded")

    monkeypatch.setattr(retrieval_service, "fts5_search", broken_fts)
    # LIKE fallback needs the same table shape the production search_transcripts uses;
    # here the real function runs against our fixture and finds the chunk.
    results = content_router._search_chunks(con, "inverse of selection probability")
    assert results and results[0]["chunk_id"] == "CHK-T-001"
