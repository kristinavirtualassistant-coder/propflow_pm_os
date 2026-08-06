import os
import sys
import json
from typing import Dict, Any

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.rbac import RBACController
from agents.leadgen_engine import LeadGenEngine
from agents.ai_subagents import MaintenanceIntakeAgent, LeadQualificationAgent

class PortalMatrixEngine:
    """Renders role-governed views across all 5 platform portals (US Configured)."""

    def __init__(self, organization_id: str = "org_pm_01"):
        self.organization_id = organization_id
        self.lead_engine = LeadGenEngine(organization_id)
        self.maint_agent = MaintenanceIntakeAgent()
        self.qual_agent = LeadQualificationAgent()

    def render_portal(self, user_role: str, portal_key: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        if not RBACController.can_access_portal(user_role, portal_key):
            return {
                "status": 403,
                "error": f"Access Denied: Role '{user_role}' cannot access Portal '{portal_key}'."
            }

        payload = payload or {}

        if portal_key == "LEAD_GEN":
            city = payload.get("city", "Austin, TX")
            leads = self.lead_engine.discover_off_market_leads(city)
            return {
                "portal": "LEAD_GEN",
                "title": "PropStream-Style DealFinder & LeadGen Portal (US)",
                "active_city": city,
                "off_market_leads_count": len(leads),
                "leads": leads
            }

        elif portal_key == "PM_ADMIN":
            return {
                "portal": "PM_ADMIN",
                "title": "Property Manager Master Command Center",
                "overview": {
                    "total_managed_properties": 12,
                    "occupancy_rate": "94%",
                    "pending_work_orders": 3,
                    "unqualified_inquiries": 5
                },
                "quick_actions": ["Dispatch Vendor", "Run US Skip-Trace", "Generate Owner Statement"]
            }

        elif portal_key == "OWNER":
            return {
                "portal": "OWNER",
                "title": "Landlord & Owner Investment Portal",
                "portfolio_summary": {
                    "monthly_gross_revenue": "$28,500.00",
                    "disbursed_this_month": "$24,200.00",
                    "reserve_fund": "$4,300.00"
                },
                "properties": ["Lone Star Condominium - Unit 101-B, Austin TX"]
            }

        elif portal_key == "TENANT":
            return {
                "portal": "TENANT",
                "title": "Tenant Resident Portal",
                "tenant_name": payload.get("tenant_name", "Sarah Jenkins"),
                "lease_status": "ACTIVE",
                "next_rent_due": "$2,200.00 on Sept 1, 2026",
                "open_tickets": []
            }

        elif portal_key == "VENDOR":
            return {
                "portal": "VENDOR",
                "title": "Contractor & Maintenance Vendor Portal",
                "assigned_jobs": [
                    {
                        "work_order_id": "wo_8841",
                        "category": "PLUMBING",
                        "priority": "EMERGENCY",
                        "location": "Unit 101-B, Lone Star Condos, Austin TX",
                        "instruction": "Fix heavy under-sink water leak."
                    }
                ]
            }

        return {"status": 404, "error": "Portal key not recognized."}

if __name__ == "__main__":
    engine = PortalMatrixEngine()
    print("[*] Rendering US LeadGen Portal...")
    print(json.dumps(engine.render_portal("ADMIN", "LEAD_GEN"), indent=2))
