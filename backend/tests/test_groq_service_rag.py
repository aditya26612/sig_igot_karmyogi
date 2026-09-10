# backend/tests/test_groq_service_rag.py
import json
import sqlite3
import pytest
from app.services import embedding_service, groq_service as gs, reranker_service, retrieval_service


@pytest.fixture()
def con(tmp_path, monkeypatch):
    # Hermeticity: never load/download the real embedding or reranker models
    # (retrieve() -> vector_search -> embedding_service.is_available() and
    #  _rerank -> reranker_service._ensure_model() would otherwise fire).
    monkeypatch.setattr(embedding_service, "_model", None)
    monkeypatch.setattr(embedding_service, "_load_failed", True)
    monkeypatch.setattr(reranker_service, "_model", None)
    monkeypatch.setattr(reranker_service, "_load_failed", True)
    c = sqlite3.connect(tmp_path / "g.sqlite")
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
    c.execute("INSERT INTO curated_lessons VALUES ('lesson-1','PL',1,'Stratified','v','u',30,'COMP-1',1)")
    c.execute("INSERT INTO curated_playlists VALUES ('PL','Sampling')")
    c.execute("""INSERT INTO transcript_chunks VALUES
        ('CHK-T-001','lesson-1','CRS-101','COMP-1','Stratified sampling',100,200,'01:40',
         'Stratified sampling divides the population into homogeneous strata.','summary','SEED')""")
    c.execute("""INSERT INTO transcript_chunks VALUES
        ('CHK-T-002','lesson-1','CRS-101','COMP-1','Weights',300,400,'05:00',
         'Sampling weights are the inverse of selection probability.','summary','SEED')""")
    retrieval_service.rebuild_fts(c)
    yield c
    c.close()


def test_ask_grounded_assistant_uses_retrieval(con, monkeypatch):
    monkeypatch.setattr(
        gs, "_llm_generate",
        lambda *a, **kw: "Stratified sampling divides the population into homogeneous strata [01:40].",
    )
    got = gs.ask_grounded_assistant("What is stratified sampling?", lang="en", con=con)
    assert got["chunk_id"] == "CHK-T-001"
    assert got["answer"].startswith("Stratified")
    assert got["timestamp_label"] == "01:40"
    assert got["source_lesson_id"] == "lesson-1"
    assert isinstance(got["suggested_actions"], list)


def test_ask_grounded_assistant_llm_down_deterministic_fallback(con, monkeypatch):
    monkeypatch.setattr(gs, "_llm_generate", lambda *a, **kw: None)
    got = gs.ask_grounded_assistant("What is stratified sampling?", lang="en", con=con)
    assert got["chunk_id"] == "CHK-T-001"  # deterministic transcript-quote fallback
    assert "homogeneous strata" in got["answer"]


def test_ask_grounded_assistant_no_match(con, monkeypatch):
    monkeypatch.setattr(gs, "_llm_generate", lambda *a, **kw: None)
    got = gs.ask_grounded_assistant("quantum thermodynamics of quarks", lang="en", con=con)
    assert got["source_lesson_id"] is None
    assert "could not find" in got["answer"].lower()


def _good_question(chunk_id, ts):
    return {
        "question_text": "What does stratified sampling do to the population for estimation?",
        "options": [
            {"text": "Divides it into homogeneous strata"},
            {"text": "Randomizes everything"},
            {"text": "Discards outliers"},
            {"text": "Clusters villages"},
        ],
        "correct_index": 0,
        "explanation": "It divides the population into homogeneous strata before sampling.",
        "difficulty": "EASY",
        "timestamp_label": ts,
        "chunk_id": chunk_id,
    }


def test_generate_quiz_questions_happy_path(monkeypatch):
    lesson = {"lesson_id": "lesson-1", "title": "Stratified", "competency_id": "COMP-1"}
    chunks = [
        {"chunk_id": "CHK-T-001", "topic": "Stratified sampling", "timestamp_label": "01:40",
         "text_content": "Stratified sampling divides the population into homogeneous strata."},
    ]
    raw = json.dumps({"questions": [_good_question("CHK-T-001", "01:40")] * 3})
    monkeypatch.setattr(gs, "_llm_generate", lambda *a, **kw: raw)

    class OfflineEmb:
        @staticmethod
        def embed_texts(texts):
            return None  # embeddings unavailable -> grounding check skipped

    monkeypatch.setattr(gs, "_embedding_probe", OfflineEmb)
    out = gs.generate_quiz_questions(lesson, chunks, num_questions=5)
    assert out is not None and len(out) == 3
    assert out[0]["chunk_id"] == "CHK-T-001"
    assert out[0]["correct_option"] == "A"


def test_generate_quiz_questions_grounding_reject(monkeypatch):
    lesson = {"lesson_id": "lesson-1", "title": "Stratified", "competency_id": "COMP-1"}
    chunks = [
        {"chunk_id": "CHK-T-001", "topic": "Stratified", "timestamp_label": "01:40",
         "text_content": "Stratified sampling divides the population into homogeneous strata."},
    ]
    off_topic = {
        "question_text": "What is the capital city of France in Europe today?",
        "options": [{"text": "Paris"}, {"text": "London"}, {"text": "Berlin"}, {"text": "Madrid"}],
        "correct_index": 0,
        "explanation": "Paris is the capital of France.",
        "difficulty": "EASY",
        "timestamp_label": "01:41",
        "chunk_id": "CHK-T-001",
    }
    raw = json.dumps({"questions": [off_topic] * 3})
    monkeypatch.setattr(gs, "_llm_generate", lambda *a, **kw: raw)

    import numpy as np

    class OrthogonalEmb:
        """Chunk text embeds to [1,0]; any question mentioning Paris embeds to [0,1]."""

        @staticmethod
        def embed_texts(texts):
            vecs = []
            for t in texts:
                v = np.array([0.0, 1.0], dtype=np.float32) if "Paris" in t else np.array(
                    [1.0, 0.0], dtype=np.float32
                )
                vecs.append(v)
            return np.vstack(vecs)

        @staticmethod
        def cosine_sim(mat, q):
            mat = np.asarray(mat, dtype=np.float32)
            q = np.asarray(q, dtype=np.float32)
            denom = np.linalg.norm(mat, axis=1) * np.linalg.norm(q)
            denom = np.where(denom == 0, 1e-12, denom)
            return (mat @ q) / denom

    monkeypatch.setattr(gs, "_embedding_probe", OrthogonalEmb)
    out = gs.generate_quiz_questions(lesson, chunks, num_questions=5)
    assert out is None  # every question failed the 0.45 grounding threshold
