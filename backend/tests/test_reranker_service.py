# backend/tests/test_reranker_service.py
from app.services import reranker_service
from app.services.reranker_service import rerank, is_available


def test_rerank_passthrough_when_unavailable(monkeypatch):
    monkeypatch.setattr(reranker_service, "_model", None)
    monkeypatch.setattr(reranker_service, "_load_failed", True)
    cands = [{"chunk_id": "A"}, {"chunk_id": "B"}]
    out = rerank("query", cands)
    assert out == cands
    assert is_available() is False


def test_rerank_sorts_by_cross_encoder_score(monkeypatch):
    class FakeModel:
        def predict(self, pairs):
            return [9.0 if "weights" in t else 1.0 for _, t in pairs]

    monkeypatch.setattr(reranker_service, "_model", FakeModel())
    monkeypatch.setattr(reranker_service, "_load_failed", False)
    cands = [
        {"chunk_id": "A", "text_content": "SQL LEFT JOIN retains all rows."},
        {"chunk_id": "B", "text_content": "Sampling weights are inverse selection probability."},
    ]
    out = rerank("what are sampling weights", cands)
    assert [c["chunk_id"] for c in out] == ["B", "A"]


def test_rerank_disabled_setting_forces_passthrough(monkeypatch):
    monkeypatch.setattr(reranker_service, "_model", None)
    monkeypatch.setattr(reranker_service, "_load_failed", False)
    monkeypatch.setattr(reranker_service.settings, "RAG_RERANKER_ENABLED", False)
    cands = [{"chunk_id": "A"}]
    assert rerank("q", cands) == cands
    assert is_available() is False
