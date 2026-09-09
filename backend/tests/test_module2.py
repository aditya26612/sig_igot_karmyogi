"""
Verification script for Module 2: Learner Experience & Core Journey APIs
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

def test_learner_apis():
    print("\n--- Testing Module 2: Learner Experience Endpoints ---")
    with TestClient(app) as client:
        # 1. Obtain JWT token for USR-001 (Aarav Sharma / Demo)
        switch_res = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
        assert switch_res.status_code == 200, f"Demo switch failed: {switch_res.text}"
        token = switch_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ Authenticated as USR-001 via demo-switch")
        
        # 2. Test GET /api/learner/me
        res = client.get("/api/learner/me", headers=headers)
        assert res.status_code == 200, f"GET /me failed: {res.text}"
        profile = res.json()
        assert profile["user_id"] == "USR-001"
        assert "Aarav" in profile["name"]
        assert "Junior Statistical Officer" in profile["current_position_name"]
        assert "Senior Statistical Officer" in profile["target_position_name"]
        print(f"✓ GET /api/learner/me verified profile: {profile['name']} ({profile['current_position_name']})")
        
        # 3. Test GET /api/learner/dashboard
        res = client.get("/api/learner/dashboard", headers=headers)
        assert res.status_code == 200, f"GET /dashboard failed: {res.text}"
        dash = res.json()
        assert "Aarav" in dash["greeting"]
        assert dash["next_action"] is not None
        print(f"✓ One Next Action: [{dash['next_action']['badge_label']}] {dash['next_action']['title']} - {dash['next_action']['subtitle']}")
        assert len(dash["priority_gaps"]) >= 1
        sampling_gap = next((g for g in dash["priority_gaps"] if g["competency_id"] == "COMP-SAMPLING"), None)
        assert sampling_gap is not None, "COMP-SAMPLING should be among priority gaps"
        print(f"✓ Priority gap found: {sampling_gap['plain_title']} (Current: L{sampling_gap['current_level']}, Required: L{sampling_gap['required_level']})")
        assert len(dash["learning_path_preview"]) > 0
        print(f"✓ Learning path preview items: {len(dash['learning_path_preview'])}")
        
        # 4. Test GET /api/learner/gaps
        res = client.get("/api/learner/gaps?scope=TARGET", headers=headers)
        assert res.status_code == 200, f"GET /gaps failed: {res.text}"
        gaps = res.json()
        assert len(gaps) >= 8
        print(f"✓ GET /api/learner/gaps returned {len(gaps)} target competency gaps")
        for g in gaps[:3]:
            print(f"   - {g['plain_title']}: Current L{g['current_level']} / Required L{g['required_level']} [Status: {g['gap_status']}]")
            
        # 5. Test GET /api/learner/learning-path
        res = client.get("/api/learner/learning-path", headers=headers)
        assert res.status_code == 200, f"GET /learning-path failed: {res.text}"
        path = res.json()
        assert "items" in path
        assert len(path["items"]) > 0
        stages = [item["stage"] for item in path["items"]]
        print(f"✓ GET /api/learner/learning-path returned {len(path['items'])} items across stages: {set(stages)}")
        
        # 6. Test GET /api/learner/career-readiness
        res = client.get("/api/learner/career-readiness", headers=headers)
        assert res.status_code == 200, f"GET /career-readiness failed: {res.text}"
        cr = res.json()
        assert "Readiness" in cr["plain_readiness_label"]
        # Verify strict guardrail: never claims promotion eligibility
        assert "promotion eligibility" in cr["notice"].lower()
        print(f"✓ GET /api/learner/career-readiness: {cr['plain_readiness_label']}")
        print(f"   Notice: {cr['notice'][:80]}...")
        
        # 7. Test unauthenticated request blocked
        unauth_res = client.get("/api/learner/dashboard")
        assert unauth_res.status_code == 401
        print("✓ Unauthenticated request properly rejected with 401 Unauthorized")

if __name__ == "__main__":
    test_learner_apis()
    print("\n==================================================")
    print("MODULE 2 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
