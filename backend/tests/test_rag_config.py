# backend/tests/test_rag_config.py
import os
import importlib

import app.config
from app.config import Settings


def test_rag_settings_defaults():
    s = Settings()
    assert s.OLLAMA_BASE_URL == "http://127.0.0.1:11434"
    assert s.OLLAMA_MODEL == "qwen2.5:1.5b"
    assert s.RAG_RERANKER_ENABLED is True
    assert s.RAG_EMBEDDING_MODEL == "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    assert s.RAG_RERANKER_MODEL == "BAAI/bge-reranker-v2-m3"
    assert s.RAG_CHUNK_TARGET_CHARS == 900
    assert s.RAG_CHUNK_OVERLAP_CHARS == 225
    assert s.GROQ_ASSISTANT_TIMEOUT_S == 8.0
    assert s.GROQ_QUIZ_TIMEOUT_S == 20.0


def test_ai_presentation_delay_env_gate():
    os.environ["AI_PRESENTATION_DELAY_SECONDS"] = "0"
    try:
        # Settings class attributes bind env vars at class-definition (import)
        # time, so a plain Settings() would not re-read the env var set above.
        # Reload the module to re-evaluate the class definition.
        importlib.reload(app.config)
        s = app.config.Settings()
        assert s.AI_PRESENTATION_DELAY_SECONDS == 0.0
    finally:
        del os.environ["AI_PRESENTATION_DELAY_SECONDS"]
        importlib.reload(app.config)
