from datetime import datetime, timezone
from typing import Dict, Any
import uuid

def create_work_order(tenant_id: str, description: str, category: str) -> Dict[str, Any]:
    urgency = "HIGH" if category.upper() in ["PLUMBING", "ELECTRICAL", "EMERGENCY", "HVAC"] else "NORMAL"
    return {
        "order_id": f"wo_{uuid.uuid4().hex[:8]}",
        "tenant_id": tenant_id,
        "description": description,
        "category": category.upper(),
        "urgency": urgency,
        "status": "OPEN",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
