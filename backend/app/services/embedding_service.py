# backend/app/services/embedding_service.py
"""Local multilingual embedding service (spec section 7).

Lazy singleton. Every public call returns None (or False) when the model is
missing so retrieval can degrade to the FTS5 leg without crashing.
"""
import logging
import threading
from typing import List, Optional

import numpy as np

from app.config import settings

logger = logging.getLogger(__name__)

_model = None
_load_failed = False
_load_lock = threading.Lock()


def _ensure_model():
    global _model, _load_failed
    if _model is not None:
        return _model
    if _load_failed:
        return None
    # Double-checked lock: the prewarm daemon and request threads can both hit
    # a cold cache; only one may pay the model load.
    with _load_lock:
        if _model is not None:
            return _model
        if _load_failed:
            return None
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(settings.RAG_EMBEDDING_MODEL)
            return _model
        except Exception as e:
            logger.warning(f"[rag] embedding model unavailable: {e}. Semantic leg disabled.")
            _load_failed = True
            return None


def is_available() -> bool:
    return _ensure_model() is not None


def embed_texts(texts: List[str]) -> Optional[np.ndarray]:
    model = _ensure_model()
    if model is None or not texts:
        return None
    try:
        return np.asarray(
            model.encode(texts, batch_size=32, show_progress_bar=False),
            dtype=np.float32,
        )
    except Exception as e:
        logger.warning(f"[rag] embed_texts failed: {e}")
        return None


def embed_query(text: str) -> Optional[np.ndarray]:
    out = embed_texts([text])
    return None if out is None else out[0]


def embedding_to_bytes(vec: np.ndarray) -> bytes:
    return np.asarray(vec, dtype=np.float32).tobytes()


def bytes_to_embedding(b: bytes) -> np.ndarray:
    return np.frombuffer(b, dtype=np.float32)


def cosine_sim(mat: np.ndarray, q: np.ndarray) -> np.ndarray:
    mat = np.asarray(mat, dtype=np.float32)
    q = np.asarray(q, dtype=np.float32)
    denom = np.linalg.norm(mat, axis=1) * np.linalg.norm(q)
    denom = np.where(denom == 0, 1e-12, denom)
    return (mat @ q) / denom
