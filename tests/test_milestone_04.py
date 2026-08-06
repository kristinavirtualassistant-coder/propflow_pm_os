import sys
import os

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.ai_subagents import LeadQualificationAgent, MaintenanceIntakeAgent, LeaseAbstractionAgent

def verify_milestone_04():
    print("=== PROPFLOW PM OS - MILESTONE 4 VERIFICATION ===")
    
    # 1. Lead Qualification Agent Check
    lead_agent = LeadQualificationAgent()
    lead_res = lead_agent.process_inquiry("Looking for a PM company for my 10 condos.")
    if lead_res["lead_type"] != "OWNER_PROSPECT":
        print("✗ Lead Qualification Sub-Agent failed classification.")
        return False
    print("✓ Lead Qualification AI Sub-Agent verified.")

    # 2. Maintenance Intake Agent Check
    maint_agent = MaintenanceIntakeAgent()
    maint_res = maint_agent.diagnose_issue("Heavy pipe leak flooding under cabinet.")
    if maint_res["category"] != "PLUMBING" or maint_res["priority"] != "EMERGENCY":
        print("✗ Maintenance Intake Sub-Agent failed diagnosis.")
        return False
    print("✓ Maintenance Intake AI Sub-Agent verified.")

    # 3. Lease Abstraction Agent Check
    lease_agent = LeaseAbstractionAgent()
    lease_res = lease_agent.parse_lease_text("Sample Lease Agreement")
    if lease_res["monthly_rent"] <= 0:
        print("✗ Lease Abstraction Sub-Agent failed extraction.")
        return False
    print("✓ Lease Abstraction AI Sub-Agent verified.")

    print("\n✓ MILESTONE 4 VERIFICATION SUCCESSFUL")
    return True

if __name__ == "__main__":
    success = verify_milestone_04()
    sys.exit(0 if success else 1)
