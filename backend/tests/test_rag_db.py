# backend/tests/test_rag_db.py
import sqlite3
from app.database import init_db


def test_rag_tables_created(tmp_path, monkeypatch):
    monkeypatch.setattr("app.database.settings.DB_PATH", tmp_path / "t.sqlite")
    init_db()
    con = sqlite3.connect(tmp_path / "t.sqlite")
    try:
        tables = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
        ).fetchall()}
    finally:
        con.close()
    assert "raw_transcripts" in tables
    assert "chunk_embeddings" in tables
    assert any("transcript_fts" in t for t in tables)
