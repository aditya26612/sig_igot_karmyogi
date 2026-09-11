# backend/tests/test_ingestion.py
import sqlite3
import pytest
from scripts.ingest_transcripts import ingest_lesson


@pytest.fixture()
def con(tmp_path):
    c = sqlite3.connect(tmp_path / "r.sqlite")
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
    c.execute("""INSERT INTO curated_lessons VALUES
        ('sampling-lesson-3','PL',1,'Stratified Sampling','vid','url',32,'COMP-SAMPLING',1)""")
    yield c
    c.close()


LESSON = {"lesson_id": "sampling-lesson-3", "title": "Stratified Sampling",
          "competency_id": "COMP-SAMPLING", "course_id": "CRS-101",
          "youtube_video_id": "vid", "duration_minutes": 32}


def test_ingest_lesson_writes_chunks_and_raw(con):
    sample = " ".join(
        f"Sentence number {i} about stratified sampling methodology." for i in range(80)
    )
    result = ingest_lesson(
        con, LESSON,
        fetcher=lambda lesson: {"text": sample, "language": "en",
                                 "source": "YOUTUBE_MANUAL", "start": 0, "end": 1920},
        embed=False,
    )
    assert result["status"] == "INGESTED"
    assert result["chunks_written"] >= 1
    rows = con.execute(
        "SELECT COUNT(*) c FROM transcript_chunks WHERE lesson_id='sampling-lesson-3'"
    ).fetchone()
    assert rows["c"] == result["chunks_written"]
    raw = con.execute(
        "SELECT status FROM raw_transcripts WHERE lesson_id='sampling-lesson-3'"
    ).fetchone()
    assert raw["status"] == "FETCHED"


def test_ingest_lesson_is_idempotent_via_cache(con):
    sample = "Some cached transcript text about stratified sampling."
    ingest_lesson(con, LESSON,
                  fetcher=lambda lesson: {"text": sample, "language": "en",
                                          "source": "YOUTUBE_MANUAL", "start": 0, "end": 1920},
                  embed=False)
    result2 = ingest_lesson(con, LESSON,
                            fetcher=lambda lesson: pytest.fail("must not refetch"),
                            embed=False)
    assert result2["status"] == "CACHED"


def test_ingest_lesson_fetch_failure_marks_failed(con):
    result = ingest_lesson(con, LESSON, fetcher=lambda lesson: None, embed=False)
    assert result["status"] == "FAILED"
    assert result["chunks_written"] == 0
    raw = con.execute(
        "SELECT status FROM raw_transcripts WHERE lesson_id='sampling-lesson-3'"
    ).fetchone()
    assert raw["status"] == "FAILED"
