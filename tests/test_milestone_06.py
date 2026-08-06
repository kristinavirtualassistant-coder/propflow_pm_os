import sys
import os

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import init_db
from models.telemetry import TelemetryLogger
from portals.portal_matrix import PortalMatrixEngine

def verify_milestone_06():
    print("=== PROPFLOW PM OS - MILESTONE 6 VERIFICATION ===")
    
    init_db()
    logger = TelemetryLogger("org_pm_01")

    # 1. Test Audit Logging
    evt_id = logger.log_event("E2E_VERIFICATION_TEST", "ADMIN", {"status": "TESTING"})
    if not evt_id.startswith("evt_"):
        print("✗ Audit telemetry failed to generate event ID.")
        return False
    print(f"✓ Telemetry audit event logged successfully ({evt_id}).")

    # 2. Verify Log Persistence
    recent_logs = logger.get_recent_logs(limit=1)
    if not recent_logs or recent_logs[0]["event_type"] != "E2E_VERIFICATION_TEST":
        print("✗ Telemetry log persistence check failed.")
        return False
    print("✓ Persistent audit log database retrieval verified.")

    print("\n✓ MILESTONE 6 VERIFICATION SUCCESSFUL")
    return True

if __name__ == "__main__":
    success = verify_milestone_06()
    sys.exit(0 if success else 1)
