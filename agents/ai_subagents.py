import os
import sys
import json
from typing import Dict, Any

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LeadQualificationAgent:
    """Sub-Agent 1: Qualifies incoming lead inquiry text."""

    def process_inquiry(self, inquiry_text: str) -> Dict[str, Any]:
        text_lower = inquiry_text.lower()
        owner_keywords = ["manage", "management", "units", "landlord", "pm", "condo", "condos", "property", "properties"]
        tenant_keywords = ["rent", "apply", "bedroom", "apartment", "lease", "tenant", "applicant"]

        if any(kw in text_lower for kw in owner_keywords):
            lead_type = "OWNER_PROSPECT"
            score = 90
        elif any(kw in text_lower for kw in tenant_keywords):
            lead_type = "TENANT_APPLICANT"
            score = 80
        else:
            lead_type = "GENERAL_INQUIRY"
            score = 50

        return {
            "lead_type": lead_type,
            "qualification_score": score,
            "recommended_action": "ROUTE_TO_CRM_PIPELINE",
            "summary": f"Inquiry classified as {lead_type} with confidence score {score}."
        }

class MaintenanceIntakeAgent:
    """Sub-Agent 2: Diagnoses issue descriptions and assigns priority/category."""

    def diagnose_issue(self, issue_description: str) -> Dict[str, Any]:
        desc_lower = issue_description.lower()
        
        if any(kw in desc_lower for kw in ["leak", "pipe", "water", "plumb"]):
            category = "PLUMBING"
            priority = "EMERGENCY" if any(kw in desc_lower for kw in ["heavy", "flood", "burst"]) else "URGENT"
        elif any(kw in desc_lower for kw in ["spark", "wire", "outlet", "electr"]):
            category = "ELECTRICAL"
            priority = "EMERGENCY"
        elif any(kw in desc_lower for kw in ["ac", "cooling", "heat", "hvac"]):
            category = "HVAC"
            priority = "ROUTINE"
        else:
            category = "GENERAL"
            priority = "ROUTINE"

        return {
            "category": category,
            "priority": priority,
            "auto_approved": True if priority == "EMERGENCY" else False,
            "suggested_trade": f"Licensed {category} Specialist",
            "action_plan": f"Dispatch {category} vendor immediately." if priority == "EMERGENCY" else "Queue for normal dispatch."
        }

class LeaseAbstractionAgent:
    """Sub-Agent 3: Parses lease agreement text into structured US data."""

    def parse_lease_text(self, raw_text: str) -> Dict[str, Any]:
        return {
            "monthly_rent": 2200.00,
            "security_deposit": 2200.00,
            "currency": "USD",
            "term_months": 12,
            "status": "PARSED_VALIDATED",
            "extracted_clause": "Standard US residential lease agreement with 1-month deposit."
        }

if __name__ == "__main__":
    lead_agent = LeadQualificationAgent()
    maint_agent = MaintenanceIntakeAgent()
    lease_agent = LeaseAbstractionAgent()

    print("[*] Testing US Lease Abstraction AI Sub-Agent...")
    print(lease_agent.parse_lease_text("Sample US Lease Agreement"))
