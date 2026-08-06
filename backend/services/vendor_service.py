from datetime import datetime, timezone
from typing import Dict, Any
import uuid

def assign_vendor_job(
    vendor_name: str,
    work_order_id: str,
    property_address: str,
    estimated_cost: float
) -> Dict[str, Any]:
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    return {
        "job_id": job_id,
        "vendor_name": vendor_name,
        "work_order_id": work_order_id,
        "property_address": property_address,
        "estimated_cost": estimated_cost,
        "status": "DISPATCHED",
        "assigned_at": datetime.now(timezone.utc).isoformat()
    }

def submit_vendor_invoice(
    job_id: str,
    labor_cost: float,
    materials_cost: float,
    owner_reserve_limit: float = 1000.0
) -> Dict[str, Any]:
    invoice_id = f"inv_{uuid.uuid4().hex[:8]}"
    total_amount = labor_cost + materials_cost
    requires_approval = total_amount > owner_reserve_limit

    return {
        "invoice_id": invoice_id,
        "job_id": job_id,
        "labor_cost": labor_cost,
        "materials_cost": materials_cost,
        "total_amount": total_amount,
        "owner_reserve_limit": owner_reserve_limit,
        "status": "REQUIRES_OWNER_APPROVAL" if requires_approval else "APPROVED_FOR_PAYMENT",
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }
