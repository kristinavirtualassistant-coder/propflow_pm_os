from datetime import datetime, timezone
from typing import Dict, Any
import uuid

def generate_lease_agreement(
    tenant_name: str,
    property_address: str,
    monthly_rent: float,
    lease_term_months: int = 12
) -> Dict[str, Any]:
    lease_id = f"lease_{uuid.uuid4().hex[:8]}"
    security_deposit = monthly_rent * 1.5
    first_month_rent = monthly_rent
    total_move_in_cost = security_deposit + first_month_rent

    return {
        "lease_id": lease_id,
        "tenant_name": tenant_name,
        "property_address": property_address,
        "monthly_rent": monthly_rent,
        "lease_term_months": lease_term_months,
        "security_deposit": security_deposit,
        "first_month_rent": first_month_rent,
        "total_move_in_cost": total_move_in_cost,
        "status": "DRAFT_PENDING_SIGNATURE",
        "signature_url": f"http://localhost:3000/e-sign/{lease_id}",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

def execute_lease_signature(lease_id: str, tenant_signature: str) -> Dict[str, Any]:
    return {
        "lease_id": lease_id,
        "tenant_signature": tenant_signature,
        "status": "EXECUTED",
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "onboarding_checklist": {
            "lease_signed": True,
            "deposit_invoice_sent": True,
            "tenant_portal_invite_sent": True,
            "key_pickup_scheduled": False
        }
    }
