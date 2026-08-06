import sys
import os

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import init_db, get_db_connection
from models.rbac import RBACController

def verify_milestone_02():
    print("=== PROPFLOW PM OS - MILESTONE 2 VERIFICATION ===")
    
    # 1. Initialize schema
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    required_tables = [
        "organizations", "users", "properties", "units", 
        "leases", "work_orders", "prospect_properties", "skip_trace_records"
    ]

    for table in required_tables:
        if table not in tables:
            print(f"✗ Database table '{table}' is missing.")
            return False
    print("✓ All 8 relational tables (including LeadGen & Skip-Trace) verified.")

    # 2. Verify RBAC boundaries
    assert RBACController.can_access_portal("ADMIN", "LEAD_GEN") is True
    assert RBACController.can_access_portal("TENANT", "PM_ADMIN") is False
    assert RBACController.can_access_portal("LANDLORD", "OWNER") is True
    print("✓ Multi-tenant RBAC portal access control rules verified.")

    print("\n✓ MILESTONE 2 VERIFICATION SUCCESSFUL")
    return True

if __name__ == "__main__":
    success = verify_milestone_02()
    sys.exit(0 if success else 1)
