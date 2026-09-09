"""
Verification script for Module 8: Admin & Supervisor Governance Portal
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

def test_admin_portal():
    print("\n--- Testing Module 8: Admin & Supervisor Governance Portal ---")
    with TestClient(app) as client:
        # 1. Role Guard: Learner cannot access Admin routes
        learner_switch = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
        assert learner_switch.status_code == 200
        learner_token = learner_switch.json()["access_token"]
        
        forbidden_res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {learner_token}"})
        assert forbidden_res.status_code == 403
        print("✓ Role guard verified: Learner rejected from Admin dashboard with 403 Forbidden")
        
        # 2. Authenticate as Admin (admin-001)
        admin_switch = client.post("/api/auth/demo-switch", json={"user_id": "admin-001"})
        assert admin_switch.status_code == 200
        admin_token = admin_switch.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        # 3. Test GET /api/admin/dashboard
        dash_res = client.get("/api/admin/dashboard", headers=admin_headers)
        assert dash_res.status_code == 200, f"Dashboard failed: {dash_res.text}"
        metrics = dash_res.json()
        assert metrics["total_learners"] >= 20
        assert metrics["total_competencies"] >= 30
        print(f"✓ GET /api/admin/dashboard verified:")
        print(f"   Total Registered Learners: {metrics['total_learners']}")
        print(f"   Official Competencies: {metrics['total_competencies']}")
        print(f"   Curated Playlists: {metrics['content_curated_playlists']} ({metrics['total_lessons']} lessons)")
        print(f"   Division Gaps: {metrics['division_gap_breakdown']}")
        
        # 4. Test GET /api/admin/learners
        learners_res = client.get("/api/admin/learners", headers=admin_headers)
        assert learners_res.status_code == 200
        learners = learners_res.json()
        assert len(learners) >= 20
        print(f"✓ GET /api/admin/learners returned {len(learners)} registered officers")
        for u in learners[:3]:
            print(f"   - {u['user_id']}: {u['name']} ({u['designation']} in {u['division_name']}) -> Readiness: {u['readiness_status']}")
            
        # 5. Test POST /api/admin/learners (Register New Learner)
        reg_payload = {
            "name": "Priya Nair",
            "email": "priya.nair@mospi.gov.in",
            "designation": "Statistical Assistant",
            "division_id": "DIV-001",
            "position_id": "POS-001",
            "target_position_id": "POS-002",
            "experience_years": 2
        }
        reg_res = client.post("/api/admin/learners", json=reg_payload, headers=admin_headers)
        assert reg_res.status_code == 200, f"Register failed: {reg_res.text}"
        reg_data = reg_res.json()
        assert "USR-" in reg_data["user_id"]
        assert reg_data["name"] == "Priya Nair"
        print(f"✓ POST /api/admin/learners registered new officer: {reg_data['user_id']} - {reg_data['name']}")
        print(f"   Message: {reg_data['message']}")
        
        # 6. Test POST /api/admin/content/upload-transcript
        upload_payload = {
            "lesson_id": "sampling-lesson-3",
            "topic": "Neyman Optimal Allocation",
            "text_content": "In Neyman optimal allocation, sample sizes within strata are allocated proportionally to stratum size and stratum standard deviation to minimize estimation variance for a fixed sample size.",
            "timestamp_label": "30:00",
            "start_seconds": 1800,
            "end_seconds": 2100
        }
        upload_res = client.post("/api/admin/content/upload-transcript", json=upload_payload, headers=admin_headers)
        assert upload_res.status_code == 200
        upload_data = upload_res.json()
        assert upload_data["status"] == "INDEXED"
        print(f"✓ POST /api/admin/content/upload-transcript indexed new administrative chunk: {upload_data['chunk_id']}")
        
        # 7. Test Question Review
        q_res = client.get("/api/admin/questions/review", headers=admin_headers)
        assert q_res.status_code == 200
        questions = q_res.json()
        assert len(questions) > 0
        target_qid = questions[0]["question_id"]
        
        rev_res = client.post(f"/api/admin/questions/{target_qid}/review", json={"is_approved": True, "review_status": "APPROVED"}, headers=admin_headers)
        assert rev_res.status_code == 200
        assert rev_res.json()["status"] == "UPDATED"
        print(f"✓ Question quality review verified for question: {target_qid}")

if __name__ == "__main__":
    test_admin_portal()
    print("\n==================================================")
    print("MODULE 8 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
