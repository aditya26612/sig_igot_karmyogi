"""
Verification script for Module 6: Learning Assistant (AI Copilot with Groq)
"""

import sys
from pathlib import Path
from contextlib import contextmanager

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db_connection
from app.services import embedding_service, reranker_service, retrieval_service

@contextmanager
def _offline_rag_models():
    """Hermeticity: disable the local embedding/reranker models for the duration of
    the test (retrieval keeps the FTS5 lexical leg only). The original module state
    is saved on entry and restored on exit (even on failure), so later live-path
    tests in the same pytest process keep the semantic-grounding stage active."""
    saved = (embedding_service._model, embedding_service._load_failed,
             reranker_service._model, reranker_service._load_failed)
    embedding_service._model, embedding_service._load_failed = None, True
    reranker_service._model, reranker_service._load_failed = None, True
    try:
        yield
    finally:
        (embedding_service._model, embedding_service._load_failed,
         reranker_service._model, reranker_service._load_failed) = saved


def test_learning_assistant():
    # Hermeticity: keep the RAG-grounded assistant offline-hermetic (no embedding /
    # reranker model loads) and give the demo DB a populated FTS5 index (demo.sqlite
    # ships with an empty transcript_fts; only scripts/ingest_transcripts.py rebuilds
    # it). Original module state is restored on exit via the context manager below,
    # so later live-path tests keep the semantic-grounding stage active.
    with _offline_rag_models():
        con = get_db_connection()
        try:
            retrieval_service.rebuild_fts(con)
        finally:
            con.close()

        print("\n--- Testing Module 6: Learning Assistant (AI Copilot) ---")
        with TestClient(app) as client:
            # Authenticate as USR-001
            switch_res = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
            assert switch_res.status_code == 200
            token = switch_res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
        
            # 1. Test GET /api/assistant/prompts
            res = client.get("/api/assistant/prompts", headers=headers)
            assert res.status_code == 200
            prompts = res.json()
            assert len(prompts) >= 4
            print(f"✓ GET /api/assistant/prompts returned {len(prompts)} quick prompt starters")
            for p in prompts[:3]:
                print(f"   - [{p['category']}] {p['label']}: '{p['prompt'][:50]}...'")
            
            # 2. Test POST /api/assistant/ask for sampling lesson
            ask_payload = {
                "question": "How is proportional sample allocation calculated across strata?",
                "context_type": "LESSON",
                "lesson_id": "sampling-lesson-3"
            }
            res = client.post("/api/assistant/ask", json=ask_payload, headers=headers)
            assert res.status_code == 200, f"Assistant ask failed: {res.text}"
            ans = res.json()
            assert len(ans["answer"]) > 20
            assert ans["timestamp_label"] is not None
            assert ans["source_lesson_title"] is not None
            assert len(ans["suggested_actions"]) > 0
            print(f"✓ POST /api/assistant/ask answered query:")
            print(f"   Source: {ans['source_lesson_title']} at [{ans['timestamp_label']}]")
            print(f"   Snippet: '{ans['citation_snippet']}'")
            print(f"   Answer: {ans['answer'][:120]}...")
            print(f"   Suggested Actions: {ans['suggested_actions'][:2]}")
        
            # 3. Test out-of-domain query rejection
            out_payload = {
                "question": "What is the secret recipe for dark chocolate cake?",
                "context_type": "GENERAL"
            }
            res = client.post("/api/assistant/ask", json=out_payload, headers=headers)
            assert res.status_code == 200
            out_ans = res.json()
            assert "not find" in out_ans["answer"].lower() or "approved" in out_ans["answer"].lower()
            print("✓ Out-of-curriculum guardrail verified: Assistant rejected non-learning query gracefully")

if __name__ == "__main__":
    test_learning_assistant()
    print("\n==================================================")
    print("MODULE 6 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
