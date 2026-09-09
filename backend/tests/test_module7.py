"""
Verification script for Module 7: iGOT Integration Simulator & Provider Abstraction
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

def test_integration_apis():
    print("\n--- Testing Module 7: iGOT Integration Simulator & Providers ---")
    with TestClient(app) as client:
        # Authenticate as Admin
        switch_res = client.post("/api/auth/demo-switch", json={"user_id": "admin-001"})
        assert switch_res.status_code == 200
        token = switch_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Test GET /api/integrations/providers
        res = client.get("/api/integrations/providers", headers=headers)
        assert res.status_code == 200
        providers = res.json()
        assert len(providers) == 3
        print(f"✓ GET /api/integrations/providers returned {len(providers)} providers:")
        for p in providers:
            print(f"   - {p['name']} [{p['badge_label']}] -> Status: {p['status']}")
            
        p_types = {p["provider_id"]: p for p in providers}
        assert p_types["YOUTUBE_CURATED"]["is_live_external"] is True
        assert p_types["IGOT_SIMULATOR"]["is_active"] is True
        assert p_types["IGOT_LIVE_CONNECTOR"]["is_active"] is False
        
        # 2. Test GET /api/integrations/igot/status
        res = client.get("/api/integrations/igot/status", headers=headers)
        assert res.status_code == 200
        status_data = res.json()
        assert status_data["simulator_status"] == "SIMULATED_HEALTHY"
        assert status_data["total_courses_in_catalog"] > 0
        print(f"✓ GET /api/integrations/igot/status: {status_data['simulator_status']} ({status_data['total_courses_in_catalog']} courses in simulated catalog)")
        print(f"   Notice: {status_data['notice']}")
        
        # 3. Test POST /api/integrations/igot/sync
        res = client.post("/api/integrations/igot/sync", headers=headers)
        assert res.status_code == 200
        sync_job = res.json()
        assert sync_job["status"] == "SUCCESS"
        assert sync_job["courses_synced"] > 0
        print(f"✓ POST /api/integrations/igot/sync executed: Job '{sync_job['job_id']}' synced {sync_job['courses_synced']} courses, {sync_job['training_records_synced']} training records")
        
        # 4. Test GET /api/integrations/sync-history
        res = client.get("/api/integrations/sync-history", headers=headers)
        assert res.status_code == 200
        history = res.json()
        assert len(history) >= 1
        print(f"✓ GET /api/integrations/sync-history returned {len(history)} recorded sync audit events")

if __name__ == "__main__":
    test_integration_apis()
    print("\n==================================================")
    print("MODULE 7 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
