import sys
import os

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from portals.portal_matrix import PortalMatrixEngine

def verify_milestone_05():
    print("=== PROPFLOW PM OS - MILESTONE 5 VERIFICATION ===")
    
    engine = PortalMatrixEngine()
    portals = ["LEAD_GEN", "PM_ADMIN", "OWNER", "TENANT", "VENDOR"]

    # 1. Verify ADMIN can access all 5 portals
    for p in portals:
        res = engine.render_portal("ADMIN", p)
        if "error" in res or res.get("portal") != p:
            print(f"✗ ADMIN access failed for portal '{p}'.")
            return False
    print("✓ ADMIN authorized access verified across all 5 Portal views.")

    # 2. Verify Security Boundaries (TENANT cannot access PM_ADMIN or LEAD_GEN)
    tenant_pm_res = engine.render_portal("TENANT", "PM_ADMIN")
    tenant_lead_res = engine.render_portal("TENANT", "LEAD_GEN")

    if tenant_pm_res.get("status") != 403 or tenant_lead_res.get("status") != 403:
        print("✗ RBAC security breach: TENANT accessed restricted admin portal.")
        return False
    
    print("✓ RBAC portal security boundary isolation verified.")
    print("\n✓ MILESTONE 5 VERIFICATION SUCCESSFUL")
    return True

if __name__ == "__main__":
    success = verify_milestone_05()
    sys.exit(0 if success else 1)
