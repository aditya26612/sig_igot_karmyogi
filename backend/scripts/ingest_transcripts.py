# backend/scripts/ingest_transcripts.py
"""One-time caption ingestion: fetch -> cache -> chunk -> FTS index -> embed (spec section 6).

Usage (from backend/):
    python -m scripts.ingest_transcripts
    python -m scripts.ingest_transcripts --lesson sampling-lesson-3
    python -m scripts.ingest_transcripts --refetch --no-embed
"""
import argparse
import random
import sqlite3
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.config import settings
from app.services import embedding_service, retrieval_service
from app.services.chunking_service import build_transcript_text, chunk_text


def _youtube_fetcher(lesson: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        fetched = api.fetch(lesson["youtube_video_id"], languages=["en", "hi"])
        segments = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in fetched
        ]
        text, start, end = build_transcript_text(segments)
        lang = getattr(fetched, "language_code", None) or "en"
        return {"text": text, "language": lang, "source": "YOUTUBE_AUTO",
                "start": start, "end": end}
    except Exception:
        return None


def ingest_lesson(
    con: sqlite3.Connection,
    lesson: Dict[str, Any],
    fetcher=None,
    embed: bool = True,
) -> Dict[str, Any]:
    lesson_id = lesson["lesson_id"]
    cached = con.execute(
        "SELECT status, transcript_text FROM raw_transcripts WHERE lesson_id = ?",
        (lesson_id,),
    ).fetchone()

    if cached and cached["status"] == "FETCHED" and cached["transcript_text"]:
        raw = cached["transcript_text"]
        start = 0
        end = int(lesson.get("duration_minutes", 30) or 30) * 60
        status = "CACHED"
    else:
        fetch = (fetcher or _youtube_fetcher)(lesson)
        if fetch is None:
            con.execute(
                "INSERT OR REPLACE INTO raw_transcripts "
                "(lesson_id, transcript_text, language, source, fetched_at, status) "
                "VALUES (?, NULL, 'en', 'YOUTUBE_AUTO', ?, 'FAILED')",
                (lesson_id, datetime.now(timezone.utc).isoformat()),
            )
            con.commit()
            return {"lesson_id": lesson_id, "status": "FAILED",
                    "chunks_written": 0, "embedding_status": "SKIPPED"}
        raw = fetch["text"]
        start = int(fetch.get("start", 0) or 0)
        default_end = start + int(lesson.get("duration_minutes", 30) or 30) * 60
        end = int(fetch.get("end", default_end) or default_end)
        con.execute(
            "INSERT OR REPLACE INTO raw_transcripts "
            "(lesson_id, transcript_text, language, source, fetched_at, status) "
            "VALUES (?, ?, ?, ?, ?, 'FETCHED')",
            (lesson_id, raw, fetch.get("language", "en"), fetch.get("source", "YOUTUBE_AUTO"),
             datetime.now(timezone.utc).isoformat()),
        )
        con.commit()
        status = "INGESTED"

    # Chunk: replace previous AUTO chunks only; CHK-DEMO-* seeds are preserved
    con.execute(
        "DELETE FROM transcript_chunks WHERE lesson_id = ? AND provenance = 'AUTO_CHUNK'",
        (lesson_id,),
    )
    chunks = chunk_text(raw, start, end, lesson_id, seq=1)
    for ch in chunks:
        con.execute(
            """INSERT OR REPLACE INTO transcript_chunks
            (chunk_id, lesson_id, course_id, competency_id, topic, start_seconds, end_seconds,
             timestamp_label, text_content, summary, provenance)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (ch["chunk_id"], lesson_id, lesson.get("course_id", "CRS-GEN"),
             lesson.get("competency_id", "COMP-GEN"), lesson.get("title", lesson_id),
             ch["start_seconds"], ch["end_seconds"], ch["timestamp_label"],
             ch["text_content"], None, "AUTO_CHUNK"),
        )
    con.commit()

    retrieval_service.rebuild_fts(con)
    embedding_status = "SKIPPED"
    if embed and chunks:
        vectors = embedding_service.embed_texts([c["text_content"] for c in chunks])
        if vectors is not None:
            now = datetime.now(timezone.utc).isoformat()
            for ch, vec in zip(chunks, vectors):
                con.execute(
                    "INSERT OR REPLACE INTO chunk_embeddings VALUES (?,?,?,?)",
                    (ch["chunk_id"], embedding_service.embedding_to_bytes(vec),
                     settings.RAG_EMBEDDING_MODEL, now),
                )
            con.commit()
            retrieval_service.embeddings_changed()
            embedding_status = "EMBEDDED"
        else:
            embedding_status = "UNAVAILABLE"

    return {"lesson_id": lesson_id, "status": status,
            "chunks_written": len(chunks), "embedding_status": embedding_status}


def run_ingestion(lesson_ids: Optional[List[str]] = None, refetch: bool = False,
                  embed: bool = True) -> List[Dict[str, Any]]:
    from app.database import get_db_connection
    con = get_db_connection()
    results: List[Dict[str, Any]] = []
    try:
        lessons = [dict(r) for r in con.execute("SELECT * FROM curated_lessons").fetchall()]
        for i, lesson in enumerate(lessons):
            if lesson_ids and lesson["lesson_id"] not in lesson_ids:
                continue
            fetched = con.execute(
                "SELECT status FROM raw_transcripts WHERE lesson_id = ?",
                (lesson["lesson_id"],),
            ).fetchone()
            if fetched and fetched["status"] == "FETCHED" and not refetch:
                continue  # resumable: skip already-ingested lessons
            if refetch:
                con.execute("DELETE FROM raw_transcripts WHERE lesson_id = ?",
                            (lesson["lesson_id"],))
                con.commit()
            results.append(ingest_lesson(con, lesson, embed=embed))
            if i < len(lessons) - 1:
                time.sleep(random.uniform(3.0, 5.0))  # per-IP rate-limit safety
    finally:
        con.close()
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", action="append", help="lesson_id (repeatable)")
    parser.add_argument("--refetch", action="store_true")
    parser.add_argument("--no-embed", action="store_true")
    args = parser.parse_args()
    for r in run_ingestion(lesson_ids=args.lesson, refetch=args.refetch,
                           embed=not args.no_embed):
        print(r)
