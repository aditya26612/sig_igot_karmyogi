# backend/tests/test_embedding_service.py
import numpy as np
import pytest
from app.services import embedding_service
from app.services.embedding_service import (
    is_available, embed_texts, embed_query,
    embedding_to_bytes, bytes_to_embedding, cosine_sim
)


def test_bytes_roundtrip():
    vec = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
    b = embedding_to_bytes(vec)
    assert isinstance(b, bytes)
    back = bytes_to_embedding(b)
    assert back.dtype == np.float32
    assert np.allclose(back, vec)


def test_cosine_sim_unit_vecs():
    mat = np.array([[1, 0], [0, 1]], dtype=np.float32)
    q = np.array([1, 0], dtype=np.float32)
    scores = cosine_sim(mat, q)
    assert scores.shape == (2,)
    assert scores[0] == pytest.approx(1.0, abs=1e-5)
    assert scores[1] == pytest.approx(0.0, abs=1e-5)


def test_unavailable_returns_none(monkeypatch):
    monkeypatch.setattr(embedding_service, "_model", None)
    monkeypatch.setattr(embedding_service, "_load_failed", True)
    assert is_available() is False
    assert embed_texts(["x"]) is None
    assert embed_query("x") is None
