# backend/app/services/reranker_service.py
"""Optional cross-encoder reranker (spec section 7). Auto-off when model missing/disabled."""
import logging
from typing import Dict, Any, List

from app.config import settings

logger = logging.getLogger(__name__)

_model = None
_load_failed = False


def _ensure_model():
    global _model, _load_failed
    if _model is not None:
        return _model
    if _load_failed or not settings.RAG_RERANKER_ENABLED:
        return None
    try:
        from sentence_transformers import CrossEncoder
        try:
            _model = CrossEncoder(settings.RAG_RERANKER_MODEL, device="cuda")
        except Exception:
            _model = CrossEncoder(settings.RAG_RERANKER_MODEL, device="cpu")
        return _model
    except Exception as e:
        logger.warning(f"[rag] reranker unavailable: {e}. Using RRF order.")
        _load_failed = True
        return None


def is_available() -> bool:
    return _ensure_model() is not None


def rerank(query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    model = _ensure_model()
    if model is None or not candidates:
        return candidates
    try:
        pairs = [(query, str(c.get("text_content", ""))) for c in candidates]
        scores = model.predict(pairs)
        order = sorted(range(len(candidates)), key=lambda i: -float(scores[i]))
        return [candidates[i] for i in order]
    except Exception as e:
        logger.warning(f"[rag] rerank failed: {e}")
        return candidates
