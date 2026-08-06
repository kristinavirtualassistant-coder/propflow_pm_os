import sys
import os
import json

from config.settings import settings
from models.database import init_db
from models.telemetry import TelemetryLogger
from portals.portal_matrix import PortalMatrixEngine
from agents.leadgen_engine import LeadGenEngine
from agents.ai_subagents import LeadQualificationAgent, MaintenanceIntakeAgent

def run_platform_demo():
    print(f"==================================================")
    print(f"   WELCOME TO {settings.APP_NAME.upper()}")
    print(f"   All-in-One Property Management Platform OS (US)")
    print(f"==================================================")
    
    # 1. Initialize System Database & Audit
    init_db()
    telemetry = TelemetryLogger(settings.ORGANIZATION_ID)
    portal_engine = PortalMatrixEngine(settings.ORGANIZATION_ID)
    lead_engine = LeadGenEngine(settings.ORGANIZATION_ID)
    maint_agent = MaintenanceIntakeAgent()

    telemetry.log_event("PLATFORM_STARTUP", "SYSTEM", {"app": settings.APP_NAME, "region": "US"})
    print("[✓] Database & Audit Telemetry Engine initialized.")

    # 2. Render LeadGen Portal (US PropStream-Style)
    print("\n--- 1. [LEAD_GEN PORTAL] US Off-Market Lead Discovery ---")
    lead_portal = portal_engine.render_portal("ADMIN", "LEAD_GEN", {"city": "Austin, TX"})
    print(f"[*] Found {lead_portal['off_market_leads_count']} off-market properties in {lead_portal['active_city']}.")
    
    if lead_portal['leads']:
        target_lead = lead_portal['leads'][0]
        print(f"[*] Selected Lead: {target_lead['address']} ({target_lead['owner_name']})")
        print("[*] Executing US Skip-Tracing...")
        trace = lead_engine.skip_trace_lead(target_lead['id'])
        print(f"[✓] Skip-Trace Output: Phone(s): {trace['phone_numbers']} | Email(s): {trace['email_addresses']}")
        telemetry.log_event("SKIP_TRACE_EXECUTED", "ADMIN", {"prospect_id": target_lead['id']})

    # 3. AI Maintenance Diagnosis Simulation
    print("\n--- 2. [MAINTENANCE AI SUB-AGENT] Maintenance Issue Intake ---")
    issue_text = "Heavy water leak in unit 101-B under kitchen sink flooding cabinets."
    print(f"[*] Incoming Ticket Description: '{issue_text}'")
    diagnosis = maint_agent.diagnose_issue(issue_text)
    print(f"[✓] AI Diagnosis: Category={diagnosis['category']} | Priority={diagnosis['priority']}")
    print(f"[✓] Action Plan: {diagnosis['action_plan']}")
    telemetry.log_event("AI_MAINTENANCE_DIAGNOSIS", "TENANT", diagnosis)

    # 4. View Portal Views Matrix
    print("\n--- 3. [PORTAL MATRIX ACCESSIBILITY SUMMARY] ---")
    roles = [("ADMIN", "PM_ADMIN"), ("LANDLORD", "OWNER"), ("TENANT", "TENANT"), ("VENDOR", "VENDOR")]
    for role, portal_key in roles:
        view = portal_engine.render_portal(role, portal_key)
        print(f"  • Role: {role:<10} | Portal: {portal_key:<10} | View Title: {view.get('title', 'N/A')}")

    print("\n==================================================")
    print("   PROPFLOW PM OS RUNNING & READY FOR US PRODUCTION")
    print("==================================================")

if __name__ == "__main__":
    run_platform_demo()
