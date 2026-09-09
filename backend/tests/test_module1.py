"""
Verification script for Module 1: Foundation, SQLite Data Layer & FastAPI Setup
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
from app.database import get_db_connection, load_db, init_db
from app.auth import seed_demo_users, verify_password
from app.engine import journey

def test_database_and_engine():
    print("\n--- 1. Testing Database & Engine Loading ---")
    init_db()
    con = get_db_connection()
    try:
        seed_demo_users(con)
        D = load_db(con)
        
        users = D.get("users", [])
        competencies = D.get("competencies", [])
        print(f"✓ Core tables loaded: {len(users)} users, {len(competencies)} competencies")
        assert len(users) == 20, f"Expected 20 users, found {len(users)}"
        assert len(competencies) >= 30, f"Expected >= 30 competencies, found {len(competencies)}"
        
        # Test Journey for USR-001 (Aarav Demo)
        j = journey(D, "USR-001")
        assert "Aarav" in j["user"]["name"]
        assert j["current_position"]["position_id"] == "POS-001"
        assert j["target_position"]["position_id"] == "POS-002"
        print(f"✓ Competency Journey for {j['user']['name']}: Current Pos: {j['current_position']['name']}, Target: {j['target_position']['name']}")
        print(f"✓ Target gaps identified: {len(j['target_gaps'])}, Priority gaps: {len(j['priority_gaps'])}")
        
        # Check that sampling is in gaps
        gap_comp_ids = [g["competency_id"] for g in j["target_gaps"]]
        assert "COMP-SAMPLING" in gap_comp_ids, "COMP-SAMPLING should be an identified target gap"
        print(f"✓ Verified priority gap COMP-SAMPLING in USR-001 target gaps")
        
        # Check app_users table
        cur = con.execute("SELECT user_id, email, full_name, role FROM app_users")
        app_users = [dict(r) for r in cur.fetchall()]
        print(f"✓ Seeded demo accounts in app_users: {len(app_users)}")
        assert len(app_users) >= 5, "Expected at least 5 demo accounts"
        for u in app_users:
            print(f"   - {u['role']}: {u['full_name']} ({u['email']})")
    finally:
        con.close()

def test_api_endpoints():
    print("\n--- 2. Testing FastAPI Endpoints ---")
    with TestClient(app) as client:
        # Health check
        res = client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        data = res.json()
        assert data["status"] == "healthy"
        print("✓ GET /health returned 200 OK, status: healthy")
        
        # Demo accounts list
        res = client.get("/api/auth/demo-accounts")
        assert res.status_code == 200
        accounts = res.json()
        assert len(accounts) == 5
        print(f"✓ GET /api/auth/demo-accounts returned {len(accounts)} accounts")
        
        # Password Login
        res = client.post("/api/auth/login", json={
            "email": "aarav.sharma@mospi.gov.in",
            "password": "LearnerPassword123!"
        })
        assert res.status_code == 200, f"Login failed: {res.text}"
        token_data = res.json()
        assert "access_token" in token_data
        assert token_data["user"]["user_id"] == "USR-001"
        print(f"✓ POST /api/auth/login successful for Aarav Sharma (JWT generated)")
        
        # Bad password
        res = client.post("/api/auth/login", json={
            "email": "aarav.sharma@mospi.gov.in",
            "password": "WrongPassword!"
        })
        assert res.status_code == 401
        print("✓ POST /api/auth/login rejected invalid credentials with 401")
        
        # Demo Switch
        res = client.post("/api/auth/demo-switch", json={"user_id": "admin-001"})
        assert res.status_code == 200
        admin_data = res.json()
        assert admin_data["user"]["role"] == "ADMIN"
        print("✓ POST /api/auth/demo-switch switched to Admin account instantly")
        
        # Profile check with token
        admin_token = admin_data["access_token"]
        res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
        assert res.status_code == 200
        profile = res.json()
        assert profile["role"] == "ADMIN"
        assert "Rajesh Kumar" in profile["full_name"]
        print(f"✓ GET /api/auth/me verified authenticated profile: {profile['full_name']}")

if __name__ == "__main__":
    test_database_and_engine()
    test_api_endpoints()
    print("\n==================================================")
    print("MODULE 1 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
