"""
Verification script for Module 3: Content Catalogue, YouTube Player & Transcripts
"""

import sys
from pathlib import Path

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

def test_content_apis():
    print("\n--- Testing Module 3: Content Catalogue & Transcripts ---")
    with TestClient(app) as client:
        # 1. Authenticate as USR-001
        switch_res = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
        assert switch_res.status_code == 200
        token = switch_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Test GET /api/content/playlists (7 playlists; COMP-030 playlist removed 2026-09-09)
        res = client.get("/api/content/playlists", headers=headers)
        assert res.status_code == 200, f"Failed: {res.text}"
        playlists = res.json()
        assert len(playlists) == 7, f"Expected 7 curated playlists, found {len(playlists)}"
        print(f"✓ GET /api/content/playlists returned all {len(playlists)} curated playlists")
        for p in playlists[:3]:
            print(f"   - {p['title']} [{p['provider_badge']}] -> Competency: {p['competency_id']}")
            assert "Curated YouTube" in p["provider_badge"]
            
        # 3. Test GET /api/content/playlists/{id}
        sampling_p_id = "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J"
        res = client.get(f"/api/content/playlists/{sampling_p_id}", headers=headers)
        assert res.status_code == 200
        p_detail = res.json()
        assert p_detail["lessons"] is not None
        assert len(p_detail["lessons"]) >= 5
        print(f"✓ GET /api/content/playlists/{sampling_p_id} returned {len(p_detail['lessons'])} ordered lessons")
        for l in p_detail["lessons"]:
            print(f"     #{l['sequence_no']}: {l['title']} ({l['duration_minutes']} min)")
            
        # 4. Test GET /api/content/lessons/sampling-lesson-3
        res = client.get("/api/content/lessons/sampling-lesson-3", headers=headers)
        assert res.status_code == 200
        lesson = res.json()
        assert lesson["lesson"]["lesson_id"] == "sampling-lesson-3"
        assert len(lesson["transcript_chunks"]) >= 2
        chk1 = lesson["transcript_chunks"][0]
        assert chk1["chunk_id"] == "CHK-DEMO-001"
        assert chk1["timestamp_label"] == "02:15"
        print(f"✓ GET /api/content/lessons/sampling-lesson-3 verified chunks: {len(lesson['transcript_chunks'])} chunks found")
        print(f"   - First chunk [{chk1['chunk_id']} @ {chk1['timestamp_label']}]: {chk1['topic']} ('{chk1['text_content'][:60]}...')")
        
        # 5. Test GET /api/content/search?q=stratified
        res = client.get("/api/content/search?q=stratified", headers=headers)
        assert res.status_code == 200
        search_res = res.json()
        assert search_res["total_matches"] >= 2
        print(f"✓ GET /api/content/search?q=stratified returned {search_res['total_matches']} matches with timestamps")
        for m in search_res["results"]:
            print(f"   - Lesson: '{m['lesson_title']}' at [{m['timestamp_label']}] -> Topic: {m['topic']}")
            print(f"     Snippet: {m['matching_snippet']}")
            
        # 6. Test POST /api/content/lessons/{id}/progress
        res = client.post("/api/content/lessons/sampling-lesson-3/progress", json={"completed": True}, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "RECORDED"
        print("✓ POST /api/content/lessons/sampling-lesson-3/progress recorded watch status")

if __name__ == "__main__":
    test_content_apis()
    print("\n==================================================")
    print("MODULE 3 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
