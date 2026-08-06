import json
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from backend.config import settings
from backend.database import SessionLocal
from backend.models import AuditLogModel

async def dispatch_event(event_type: str, description: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # 1. Persist event into SQLite audit_logs table
    db = SessionLocal()
    try:
        log_entry = AuditLogModel(
            id=f"audit_{int(datetime.now().timestamp()*1000)}",
            event_type=event_type,
            description=description,
            timestamp=timestamp,
            payload=json.dumps(payload)
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error persisting audit log: {e}")
    finally:
        db.close()

    # 2. Forward payload to Make.com / External Webhook if URL is configured
    webhook_status = "SKIPPED"
    if settings.MAKE_WEBHOOK_URL:
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(
                    settings.MAKE_WEBHOOK_URL,
                    json={
                        "event_type": event_type,
                        "description": description,
                        "timestamp": timestamp,
                        "payload": payload
                    },
                    timeout=5.0
                )
                webhook_status = f"DELIVERED ({res.status_code})"
            except Exception as e:
                webhook_status = f"FAILED ({str(e)})"

    return {
        "event_type": event_type,
        "timestamp": timestamp,
        "db_persisted": True,
        "webhook_status": webhook_status
    }
