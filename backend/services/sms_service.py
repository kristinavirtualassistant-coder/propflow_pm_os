from typing import Dict, Any
from backend.database import SessionLocal
from backend.models import LeadModel, AuditLogModel
from datetime import datetime, timezone

def process_inbound_sms(from_number: str, message_body: str) -> Dict[str, Any]:
    db = SessionLocal()
    auto_reply = "Thank you for contacting PropFlow PM OS! A property manager will get back to you shortly."
    
    try:
        lead = db.query(LeadModel).filter(LeadModel.phone == from_number).first()
        body_lower = message_body.lower().strip()
        
        if "rent" in body_lower or "available" in body_lower:
            auto_reply = "Thanks for inquiring! View our current available listings and submit applications at http://localhost:3000."
        elif "repair" in body_lower or "maintenance" in body_lower:
            auto_reply = "Your maintenance request has been noted. Please submit a work order through your tenant portal."

        if lead:
            lead.status = "CONTACTED"

        audit = AuditLogModel(
            id=f"sms_{int(datetime.now(timezone.utc).timestamp()*1000)}",
            event_type="INBOUND_SMS_RECEIVED",
            description=f"SMS from {from_number}: {message_body}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload={"from": from_number, "body": message_body, "auto_reply": auto_reply}
        )
        db.add(audit)
        db.commit()
    except Exception:
        db.rollback()
        audit = AuditLogModel(
            id=f"sms_{int(datetime.now(timezone.utc).timestamp()*1000)}",
            event_type="INBOUND_SMS_RECEIVED",
            description=f"SMS from {from_number}: {message_body}",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        db.add(audit)
        db.commit()
    finally:
        db.close()

    return {
        "status": "success",
        "from": from_number,
        "message": message_body,
        "auto_reply": auto_reply
    }
