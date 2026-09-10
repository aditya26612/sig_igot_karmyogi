# backend/tests/test_chunking.py
from app.config import settings
from app.services.chunking_service import (
    chunk_text, merge_near_duplicate_hits, format_ts, build_transcript_text
)


def test_format_ts():
    assert format_ts(135) == "02:15"
    assert format_ts(0) == "00:00"


def test_build_transcript_text():
    segments = [
        {"text": "Stratified sampling ", "start": 10, "duration": 5},
        {"text": "divides the population.", "start": 20, "duration": 4},
    ]
    text, s, e = build_transcript_text(segments)
    assert text == "Stratified sampling divides the population."
    assert (s, e) == (10, 24)


def test_chunk_text_short_transcript_single_chunk():
    chunks = chunk_text("short text", 0, 30, "x-lesson", 1)
    assert len(chunks) == 1
    assert chunks[0]["chunk_id"] == "CHK-X-LESSON-001"
    assert chunks[0]["provenance"] == "AUTO_CHUNK"


def test_chunk_text_coverage_overlap_determinism():
    text = ("word " * 400).strip()  # ~2000 chars
    chunks = chunk_text(text, 0, 300, "sampling-lesson-3", 1)
    assert len(chunks) >= 3
    for i in range(len(chunks) - 1):
        # Overlap: the tail of chunk i reappears in chunk i+1
        tail = chunks[i]["text_content"][-settings.RAG_CHUNK_OVERLAP_CHARS:]
        assert tail in chunks[i + 1]["text_content"]
        # Coverage: no character gap between consecutive chunks
        assert chunks[i + 1]["start_offset"] <= chunks[i]["end_offset"]
    # Determinism: identical inputs -> identical chunk IDs
    chunks2 = chunk_text(text, 0, 300, "sampling-lesson-3", 1)
    assert [c["chunk_id"] for c in chunks] == [c["chunk_id"] for c in chunks2]


def test_merge_near_duplicate_hits_boundary_strict():
    # A(100-200) vs B(150-250): overlap 50s, smaller duration 100s -> 0.50, NOT > 0.5 -> both kept
    a = {"chunk_id": "A", "lesson_id": "L", "start_seconds": 100, "end_seconds": 200}
    b = {"chunk_id": "B", "lesson_id": "L", "start_seconds": 150, "end_seconds": 250}
    c = {"chunk_id": "C", "lesson_id": "L", "start_seconds": 400, "end_seconds": 500}
    d = {"chunk_id": "D", "lesson_id": "M", "start_seconds": 100, "end_seconds": 200}
    merged = merge_near_duplicate_hits([a, b, c, d])
    ids = [x["chunk_id"] for x in merged]
    assert set(ids) == {"A", "B", "C", "D"}  # boundary keeps both; different lesson never merged
    # Deep overlap DOES merge: E(400-500) vs c(400-500) identical range
    e = {"chunk_id": "E", "lesson_id": "L", "start_seconds": 400, "end_seconds": 500}
    merged2 = merge_near_duplicate_hits([c, e])
    assert [x["chunk_id"] for x in merged2] == ["C"]
