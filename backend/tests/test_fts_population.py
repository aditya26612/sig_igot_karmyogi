# backend/tests/test_fts_population.py
"""C1 regression: the FTS5 index must be populated by every production path that
writes transcript chunks — server startup (lifespan), reset_demo, and the admin
upload endpoint. Found by the final whole-branch review: rebuild_fts's only
non-test caller was the ingestion CLI, so a fresh clone's copilot retrieved
nothing despite seeded curriculum chunks.
"""
import sqlite3
import pytest

from app.config import settings
from app.database import init_db, get_db_connection
from app.services import retrieval_service


@pytest.fixture()
def prod_con(tmp_path, monkeypatch):
    """A production-shaped DB in tmp_path: full init_db schema (which creates
    transcript_fts), production connection settings — no hand-built subset."""
    db_file = tmp_path / "prod.sqlite"
    monkeypatch.setattr(settings, "DB_PATH", str(db_file))
    init_db()
    con = get_db_connection()
    yield con
    con.close()


def test_startup_seeds_fts_from_chunks(prod_con):
    # The lifespan flow on a fresh DB: seed_and_index must both seed the
    # curriculum chunks AND leave them searchable via the FTS index.
    from app import main as app_main

    app_main.seed_and_index(prod_con)
    n_chunks = prod_con.execute("SELECT COUNT(*) FROM transcript_chunks").fetchone()[0]
    n_fts = prod_con.execute("SELECT COUNT(*) FROM transcript_fts").fetchone()[0]
    assert n_chunks > 0, "seed_content_catalogue should seed transcript chunks"
    assert n_fts == n_chunks, "every seeded chunk must be in the FTS index"
    hits = retrieval_service.fts5_search(prod_con, "stratified sampling")
    assert hits, "seeded chunks must be retrievable through FTS5 after startup"


def test_admin_upload_indexes_chunk(prod_con):
    # The admin upload path must keep transcript_fts in sync: after its
    # transcript_chunks insert, the chunk must be retrievable via FTS5.
    from app.routers import admin_router

    app_main_seed = pytest.importorskip("app.main")
    app_main_seed.seed_and_index(prod_con)

    chunk_id = "CHK-ADM-test001"
    with prod_con:
        prod_con.execute(
            """INSERT INTO transcript_chunks (
                chunk_id, lesson_id, course_id, competency_id, topic,
                start_seconds, end_seconds, timestamp_label, text_content, summary, provenance)
            VALUES (?, 'sampling-lesson-1', 'CRS-1', 'COMP-SAMPLING', ?,
                    0, 90, '00:00', ?, '', 'ADMIN_UPLOAD')""",
            (chunk_id, "admin upload", "Administratively uploaded household survey frame content."),
        )
        admin_router._index_uploaded_chunk(prod_con, chunk_id)
    hits = retrieval_service.fts5_search(prod_con, "household survey frame")
    assert any(h["chunk_id"] == chunk_id for h in hits)
