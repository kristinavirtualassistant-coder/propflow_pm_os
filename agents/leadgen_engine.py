import os
import sys
import json
import uuid
from typing import Dict, Any, List

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import get_db_connection

class LeadGenEngine:
    """PropStream-style Lead Discovery and Skip-Tracing Engine (US Market)."""

    def __init__(self, organization_id: str = "org_pm_01"):
        self.organization_id = organization_id

    def discover_off_market_leads(self, city: str = "Austin, TX", distress_tag: str = "ABSENTEE_OWNER") -> List[Dict[str, Any]]:
        """Searches US off-market property leads filtered by distress tags."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert realistic US off-market property leads if database is empty for this query
        cursor.execute("SELECT COUNT(*) FROM prospect_properties WHERE city = ? AND organization_id = ?", (city, self.organization_id))
        count = cursor.fetchone()[0]

        if count == 0:
            mock_leads = [
                (f"lead_{uuid.uuid4().hex[:6]}", self.organization_id, "4500 Congress Ave", city, "Apex Lone Star Holdings LLC", "LLC", 450000.0, json.dumps(["ABSENTEE_OWNER", "HIGH_EQUITY"]), "NEW"),
                (f"lead_{uuid.uuid4().hex[:6]}", self.organization_id, "8804 South Lamar Blvd", city, "Robert Miller", "INDIVIDUAL", 280000.0, json.dumps(["VACANT", "TAX_DELINQUENT"]), "NEW")
            ]
            cursor.executemany("""
                INSERT INTO prospect_properties (id, organization_id, address, city, owner_name, owner_type, estimated_equity, distress_tags, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, mock_leads)
            conn.commit()

        cursor.execute("SELECT * FROM prospect_properties WHERE city = ? AND organization_id = ?", (city, self.organization_id))
        rows = cursor.fetchall()
        conn.close()

        leads = []
        for row in rows:
            leads.append({
                "id": row["id"],
                "address": row["address"],
                "city": row["city"],
                "owner_name": row["owner_name"],
                "owner_type": row["owner_type"],
                "estimated_equity": row["estimated_equity"],
                "distress_tags": json.loads(row["distress_tags"]) if row["distress_tags"] else [],
                "status": row["status"]
            })
        return leads

    def skip_trace_lead(self, prospect_id: str) -> Dict[str, Any]:
        """Performs skip-tracing to unmask owner contact details (US Phone Numbers + Emails)."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM prospect_properties WHERE id = ?", (prospect_id,))
        prospect = cursor.fetchone()

        if not prospect:
            conn.close()
            return {"error": f"Lead ID '{prospect_id}' not found."}

        owner_name = prospect["owner_name"]
        
        # Simulate US corporate registry unmasking & US consumer phone lookup (+1 512 Area Code)
        if prospect["owner_type"] == "LLC":
            unmasked_contact = f"Manager: Robert Miller (via {owner_name})"
            phones = ["+1 (512) 555-0199", "+1 (512) 555-0188"]
            emails = ["rmiller@apexlonestar.com", "contact@apexlonestar.com"]
        else:
            unmasked_contact = owner_name
            phones = ["+1 (737) 555-0142"]
            emails = [f"{owner_name.lower().replace(' ', '.')}@gmail.com"]

        skip_trace_id = f"st_{uuid.uuid4().hex[:6]}"
        cursor.execute("""
            INSERT INTO skip_trace_records (id, prospect_property_id, phone_numbers, email_addresses)
            VALUES (?, ?, ?, ?)
        """, (skip_trace_id, prospect_id, json.dumps(phones), json.dumps(emails)))

        cursor.execute("UPDATE prospect_properties SET status = 'SKIP_TRACED' WHERE id = ?", (prospect_id,))
        conn.commit()
        conn.close()

        return {
            "prospect_id": prospect_id,
            "owner_name": owner_name,
            "unmasked_contact": unmasked_contact,
            "phone_numbers": phones,
            "email_addresses": emails,
            "status": "SKIP_TRACED"
        }

if __name__ == "__main__":
    engine = LeadGenEngine()
    print("[*] Testing US Off-Market Lead Discovery...")
    leads = engine.discover_off_market_leads("Austin, TX")
    print(f"[✓] Discovered {len(leads)} off-market leads.")
    if leads:
        print("[*] Testing Skip-Tracing on First Lead...")
        trace_result = engine.skip_trace_lead(leads[0]["id"])
        print("[✓] Skip-Trace Output:", json.dumps(trace_result, indent=2))
