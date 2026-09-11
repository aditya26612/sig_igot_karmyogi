# backend/app/services/chunking_service.py
"""Overlapping chunker for video transcripts (spec section 6)."""
from typing import Any, Dict, List, Tuple

from app.config import settings


def format_ts(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def build_transcript_text(segments: List[Dict[str, Any]]) -> Tuple[str, int, int]:
    """Joins caption segments [{text, start, duration}, ...] into continuous text."""
    parts: List[str] = []
    first_start = segments[0]["start"] if segments else 0
    last_end = first_start
    for seg in segments:
        parts.append(str(seg.get("text", "")).strip())
        last_end = max(last_end, seg["start"] + seg.get("duration", 0))
    return " ".join(p for p in parts if p), int(first_start), int(last_end)


def chunk_text(
    text: str,
    start_seconds: int,
    end_seconds: int,
    lesson_id: str,
    seq: int = 1,
) -> List[Dict[str, Any]]:
    """
    Sliding-window overlapping chunker (spec section 6).

    Window ~RAG_CHUNK_TARGET_CHARS with ~RAG_CHUNK_OVERLAP_CHARS overlap; windows
    prefer to break at whitespace in the last 15% of the window. Chunks carry
    start_offset/end_offset (character positions, for coverage/determinism tests)
    plus interpolated start_seconds/end_seconds.
    """
    text = (text or "").strip()
    if not text:
        return []
    target = settings.RAG_CHUNK_TARGET_CHARS
    overlap = settings.RAG_CHUNK_OVERLAP_CHARS
    duration = max(int(end_seconds) - int(start_seconds), 1)
    n = len(text)
    prefix = lesson_id.upper()

    chunks: List[Dict[str, Any]] = []
    pos = 0
    step = seq
    while pos < n:
        window = text[pos:pos + target]
        if pos + target < n and len(window) > overlap:
            # Prefer a whitespace break in the final 15% of the window
            soft = int(len(window) * 0.85)
            cut = len(window)
            for sp in range(len(window) - 1, soft, -1):
                if window[sp] == " ":
                    cut = sp
                    break
            window = window[:cut]
        start_off = pos
        end_off = pos + len(window)
        c_start = start_seconds + int(start_off / n * duration)
        c_end = start_seconds + int(min(end_off, n) / n * duration)
        chunks.append({
            "chunk_id": f"CHK-{prefix}-{step:03d}",
            "lesson_id": lesson_id,
            "topic": "",
            "start_seconds": c_start,
            "end_seconds": c_end,
            "timestamp_label": format_ts(c_start),
            "text_content": window.strip(),
            "start_offset": start_off,
            "end_offset": end_off,
            "provenance": "AUTO_CHUNK",
        })
        step += 1
        if pos + target >= n:
            break
        pos += max(len(window) - overlap, 1)
    return chunks


def merge_near_duplicate_hits(
    hits: List[Dict[str, Any]], overlap_fraction: float = 0.5
) -> List[Dict[str, Any]]:
    """Drops later hits whose time range overlaps >overlap_fraction of the smaller chunk."""
    kept: List[Dict[str, Any]] = []
    for h in hits:
        dropped = False
        for k in kept:
            if h.get("lesson_id") != k.get("lesson_id"):
                continue
            hs, he = h.get("start_seconds", 0), h.get("end_seconds", 0)
            ks, ke = k.get("start_seconds", 0), k.get("end_seconds", 0)
            ov = max(0, min(he, ke) - max(hs, ks))
            smaller = min(he - hs, ke - ks)
            if smaller > 0 and ov / smaller > overlap_fraction:
                dropped = True
                break
        if not dropped:
            kept.append(h)
    return kept
