import sys
import os

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import init_db
from agents.leadgen_engine import LeadGenEngine

def verify_milestone_03():
    print("=== PROPFLOW PM OS - MILESTONE 3 VERIFICATION ===")
    
    init_db()
    engine = LeadGenEngine(organization_id="org_pm_01")

    # 1. Test Lead Discovery
    leads = engine.discover_off_market_leads("Quezon City")
    if not leads or len(leads) == 0:
        print("✗ Lead discovery failed to return off-market leads.")
        return False
    print(f"✓ Lead Discovery Engine retrieved {len(leads)} off-market properties.")

    # 2. Test Skip-Tracing
    target_lead_id = leads[0]["id"]
    trace_result = engine.skip_trace_lead(target_lead_id)

    if "phone_numbers" not in trace_result or len(trace_result["phone_numbers"]) == 0:
        print("✗ Skip-tracing failed to extract phone numbers.")
        return False
    
    print(f"✓ Skip-Tracing Engine unmasked lead '{target_lead_id}': {trace_result['phone_numbers']}")
    print("\n✓ MILESTONE 3 VERIFICATION SUCCESSFUL")
    return True

if __name__ == "__main__":
    success = verify_milestone_03()
    sys.exit(0 if success else 1)
