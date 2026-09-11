# backend/tests/eval_retrieval.py
"""Golden-set retrieval eval (spec section 11): like vs fts5 vs hybrid vs hybrid+rerank.

Run from backend/:  python -m tests.eval_retrieval
"""
import json
import sys
from pathlib import Path

from app.database import get_db_connection
from app.services import reranker_service, retrieval_service as rs
from app.services.transcript_service import search_transcripts_keywords

GOLDEN = Path(__file__).resolve().parents[1] / "data" / "golden_set.json"
KS = (1, 3, 5)


def hit_metrics(ranked_ids, expected):
    hits = {k: int(expected in ranked_ids[:k]) for k in KS}
    mrr = 0.0
    if expected in ranked_ids:
        mrr = 1.0 / (ranked_ids.index(expected) + 1)
    return hits, mrr


def run_config(name, fn, items):
    agg = {k: 0 for k in KS}
    mrr_sum = 0.0
    for it in items:
        ids = fn(it["query"])
        hits, mrr = hit_metrics(ids, it["expected_chunk_id"])
        for k in KS:
            agg[k] += hits[k]
        mrr_sum += mrr
    n = len(items)
    return {**{f"hit@{k}": agg[k] / n for k in KS}, "MRR": mrr_sum / n}


def evaluate():
    items = json.loads(GOLDEN.read_text(encoding="utf-8"))
    con = get_db_connection()
    try:
        table = {}

        table["like"] = run_config(
            "like",
            lambda q: [h["chunk_id"] for h in search_transcripts_keywords(con, q, limit=5)],
            items,
        )
        table["fts5"] = run_config(
            "fts5",
            lambda q: [h["chunk_id"] for h in rs.fts5_search(con, q, limit=5)],
            items,
        )

        # hybrid (reranker forced OFF)
        saved_model, saved_failed = reranker_service._model, reranker_service._load_failed
        reranker_service._model, reranker_service._load_failed = None, True
        table["hybrid"] = run_config(
            "hybrid", lambda q: [h["chunk_id"] for h in rs.retrieve(q, top_k=5, con=con)], items,
        )
        # hybrid+rerank (reranker restored; loads on demand if available)
        reranker_service._model, reranker_service._load_failed = saved_model, False
        table["hybrid+rerank"] = run_config(
            "hybrid+rerank",
            lambda q: [h["chunk_id"] for h in rs.retrieve(q, top_k=5, con=con)],
            items,
        )
    finally:
        con.close()

    print(f"{'config':<16}{'hit@1':>8}{'hit@3':>8}{'hit@5':>8}{'MRR':>8}")
    for name, m in table.items():
        print(f"{name:<16}{m['hit@1']:>8.2f}{m['hit@3']:>8.2f}{m['hit@5']:>8.2f}{m['MRR']:>8.2f}")

    if table["hybrid"]["hit@5"] < table["like"]["hit@5"]:
        print("REGRESSION: hybrid hit@5 below LIKE baseline")
        sys.exit(1)


if __name__ == "__main__":
    evaluate()
