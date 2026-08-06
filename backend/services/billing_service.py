from datetime import datetime, timezone
from typing import Dict, Any

def calculate_tenant_balance(tenant_id: str, base_rent: float, days_late: int) -> Dict[str, Any]:
    late_fee = 0.0
    if days_late > 5:
        late_fee = 50.0 + (10.0 * (days_late - 5))
    
    total_due = base_rent + late_fee
    return {
        "tenant_id": tenant_id,
        "base_rent": base_rent,
        "days_late": days_late,
        "late_fee": late_fee,
        "total_due": total_due,
        "status": "OVERDUE" if days_late > 0 else "CURRENT",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
