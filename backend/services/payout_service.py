from datetime import datetime, timezone
from typing import Dict, Any, List
import uuid

def calculate_owner_payout(
    owner_id: str,
    property_address: str,
    gross_rent_collected: float,
    management_fee_pct: float = 10.0,
    maintenance_expenses: float = 0.0,
    reserve_holdback: float = 250.0
) -> Dict[str, Any]:
    management_fee = gross_rent_collected * (management_fee_pct / 100.0)
    net_payout = gross_rent_collected - management_fee - maintenance_expenses - reserve_holdback
    if net_payout < 0:
        net_payout = 0.0

    return {
        "statement_id": f"stmt_{uuid.uuid4().hex[:8]}",
        "owner_id": owner_id,
        "property_address": property_address,
        "gross_rent_collected": gross_rent_collected,
        "management_fee": management_fee,
        "management_fee_pct": management_fee_pct,
        "maintenance_expenses": maintenance_expenses,
        "reserve_holdback": reserve_holdback,
        "net_payout": net_payout,
        "status": "CALCULATED",
        "period": datetime.now(timezone.utc).strftime("%Y-%m")
    }

def generate_ach_batch_export(payout_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    batch_id = f"ach_{uuid.uuid4().hex[:8]}"
    total_batch_amount = sum(record.get("net_payout", 0.0) for record in payout_records)
    
    nacha_header = f"101 011000015 {batch_id} {datetime.now(timezone.utc).strftime('%y%m%d%H%M')} A094101"
    
    return {
        "batch_id": batch_id,
        "total_records": len(payout_records),
        "total_batch_amount": total_batch_amount,
        "nacha_header": nacha_header,
        "payouts": payout_records,
        "status": "READY_FOR_BANK_SUBMISSION",
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
