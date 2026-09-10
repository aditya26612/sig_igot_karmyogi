# backend/app/services/retrieval_service.py
"""Hybrid retrieval (spec section 7): FTS5 BM25 + vector cosine, RRF fusion,
near-duplicate merge, optional reranker stage."""
import logging
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from app.services import embedding_service
from app.services.chunking_service import merge_near_duplicate_hits
from app.services.transcript_service import extract_question_keywords

logger = logging.getLogger(__name__)

_LEG_LIMIT = 20
_RRF_K = 60


def _scope_clause(lesson_id: Optional[str], competency_id: Optional[str]) -> Tuple[str, list]:
    clause = ""
    params: List[Any] = []
    if lesson_id:
        clause += " AND c.lesson_id = ? "
        params.append(lesson_id)
    if competency_id:
        clause += " AND c.competency_id = ? "
        params.append(competency_id)
    return clause, params


def _expand_query(query: str) -> str:
    """Hindi->English lexical expansion + stopword removal via existing helpers."""
    keywords = extract_question_keywords(query, max_terms=8)
    return " ".join(keywords) if keywords else query


def fts5_search(
    con: sqlite3.Connection,
    query: str,
    lesson_id: Optional[str] = None,
    competency_id: Optional[str] = None,
    limit: int = _LEG_LIMIT,
) -> List[Dict[str, Any]]:
    expanded = _expand_query(query)
    terms = [t for t in expanded.split() if t]
    if not terms:
        return []
    fts_query = " OR ".join(terms)
    clause, params = _scope_clause(lesson_id, competency_id)
    sql = f"""
    SELECT c.chunk_id, c.lesson_id, c.course_id, c.competency_id, c.topic,
           c.timestamp_label, c.start_seconds, c.end_seconds, c.text_content, c.summary,
           l.title as lesson_title, p.title as playlist_title
    FROM transcript_fts f
    JOIN transcript_chunks c ON c.chunk_id = f.chunk_id
    LEFT JOIN curated_lessons l ON c.lesson_id = l.lesson_id
    LEFT JOIN curated_playlists p ON l.playlist_id = p.playlist_id
    WHERE transcript_fts MATCH ? {clause}
    ORDER BY rank
    LIMIT ?
    """
    try:
        cursor = con.execute(sql, [fts_query] + params + [limit])
    except sqlite3.OperationalError:
        return []
    return [dict(r) for r in cursor.fetchall()]


# ---- vector leg ----
_matrix_cache: Optional[Dict[str, Any]] = None


def embeddings_changed() -> None:
    global _matrix_cache
    _matrix_cache = None


def _vector_ids_and_matrix(con: sqlite3.Connection) -> Tuple[Optional[List[str]], Optional[np.ndarray]]:
    """Returns (ids, matrix) over all embedded chunks; cached until embeddings_changed()."""
    global _matrix_cache
    if _matrix_cache is not None:
        return _matrix_cache["ids"], _matrix_cache["matrix"]
    rows = con.execute("SELECT chunk_id, embedding FROM chunk_embeddings").fetchall()
    if not rows:
        _matrix_cache = {"ids": [], "matrix": None}
        return [], None
    ids = [r["chunk_id"] for r in rows]
    matrix = np.vstack([np.frombuffer(r["embedding"], dtype=np.float32) for r in rows])
    _matrix_cache = {"ids": ids, "matrix": matrix}
    return ids, matrix


def vector_search(
    con: sqlite3.Connection,
    query: str,
    lesson_id: Optional[str] = None,
    competency_id: Optional[str] = None,
    leg_limit: int = _LEG_LIMIT,
) -> List[Dict[str, Any]]:
    if not embedding_service.is_available():
        return []
    qvec = embedding_service.embed_query(query)
    if qvec is None:
        return []
    ids, matrix = _vector_ids_and_matrix(con)
    if not ids or matrix is None:
        return []
    scores = embedding_service.cosine_sim(matrix, qvec)
    order = np.argsort(-scores)[:leg_limit]
    top_ids = [ids[i] for i in order]
    if not top_ids:
        return []
    clause, params = _scope_clause(lesson_id, competency_id)
    placeholders = ",".join("?" * len(top_ids))
    sql = f"""
    SELECT c.chunk_id, c.lesson_id, c.course_id, c.competency_id, c.topic,
           c.timestamp_label, c.start_seconds, c.end_seconds, c.text_content, c.summary,
           l.title as lesson_title, p.title as playlist_title
    FROM transcript_chunks c
    LEFT JOIN curated_lessons l ON c.lesson_id = l.lesson_id
    LEFT JOIN curated_playlists p ON l.playlist_id = p.playlist_id
    WHERE c.chunk_id IN ({placeholders}) {clause}
    """
    try:
        rows = {r["chunk_id"]: dict(r) for r in con.execute(sql, top_ids + params).fetchall()}
    except sqlite3.OperationalError:
        return []
    return [rows[cid] for cid in top_ids if cid in rows]


def rrf_fuse(lex_ids: List[str], sem_ids: List[str], k: int = _RRF_K) -> List[str]:
    scores: Dict[str, float] = {}
    for leg in (lex_ids, sem_ids):
        for rank, cid in enumerate(leg, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)


def retrieve(
    query: str,
    lesson_id: Optional[str] = None,
    competency_id: Optional[str] = None,
    top_k: int = 4,
    con: sqlite3.Connection = None,
) -> List[Dict[str, Any]]:
    """Hybrid retrieve -> RRF fusion -> near-dup merge -> rerank -> top_k."""
    should_close = con is None
    if should_close:
        from app.database import get_db_connection
        con = get_db_connection()
    try:
        lex = fts5_search(con, query, lesson_id, competency_id)
        sem = vector_search(con, query, lesson_id, competency_id)
        fused_ids = rrf_fuse([h["chunk_id"] for h in lex], [h["chunk_id"] for h in sem])
        if not fused_ids:
            return []
        by_id: Dict[str, Dict[str, Any]] = {}
        for h in lex + sem:
            by_id.setdefault(h["chunk_id"], h)
        ranked = [by_id[cid] for cid in fused_ids if cid in by_id]
        ranked = merge_near_duplicate_hits(ranked)
        ranked = _rerank(query, ranked)[:20]
        return ranked[:top_k]
    finally:
        if should_close:
            con.close()


def _rerank(query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Reranker stage; pass-through stub replaced in Task 8."""
    return candidates


def rebuild_fts(con: sqlite3.Connection) -> None:
    """Repopulates transcript_fts from transcript_chunks; idempotent."""
    with con:
        con.execute("DELETE FROM transcript_fts")
        con.execute("""
        INSERT INTO transcript_fts (chunk_id, text_content, topic)
        SELECT chunk_id, text_content, COALESCE(topic, '')
        FROM transcript_chunks
        """)
