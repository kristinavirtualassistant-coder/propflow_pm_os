import os
import json
import sqlite3
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="PropFlow PM OS - Core Engine",
    version="1.0.0",
    description="Enterprise Property Management OS API Service"
)

# Get CORS origins safely from environment or fallback to local defaults
cors_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,*")
allowed_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.getenv("DATABASE_URL", "sqlite:////tmp/propflow.db").replace("sqlite:///", "")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class EventDispatchSchema(BaseModel):
    event_type: str
    description: str
    payload: Optional[Dict[str, Any]] = None

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/api/v1/events/dispatch")
def dispatch_event(event: EventDispatchSchema, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AUDIT_LOGS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            description TEXT,
            payload TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute(
        "INSERT INTO AUDIT_LOGS (event_type, description, payload) VALUES (?, ?, ?)",
        (event.event_type, event.description, json.dumps(event.payload or {}))
    )
    db.commit()
    return {"status": "success", "event_type": event.event_type}

# --- MILESTONE 2: VAPI AI VOICE AGENT WEBHOOK HANDLERS ---

@app.post("/api/v1/webhooks/vapi")
async def vapi_webhook_handler(request: Request, db: sqlite3.Connection = Depends(get_db)):
    """
    Handles real-time inbound call payloads from Vapi AI Voice Engine.
    Processes: end-of-call report, transcript analysis, and lead/maintenance routing.
    """
    try:
        payload = await request.json()
        message = payload.get("message", {})
        message_type = message.get("type")

        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CALL_LOGS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                call_id TEXT UNIQUE,
                phone_number TEXT,
                transcript TEXT,
                summary TEXT,
                category TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        if message_type == "end-of-call-report":
            call_id = message.get("call", {}).get("id", "N/A")
            customer_phone = message.get("customer", {}).get("number", "Unknown")
            transcript = message.get("transcript", "")
            summary = message.get("summary", "")
            
            category = "GENERAL_INQUIRY"
            if "leak" in transcript.lower() or "repair" in transcript.lower() or "broken" in transcript.lower():
                category = "MAINTENANCE_REQUEST"
            elif "rent" in transcript.lower() or "available" in transcript.lower() or "lease" in transcript.lower():
                category = "LEAD_QUALIFICATION"

            cursor.execute("""
                INSERT OR REPLACE INTO CALL_LOGS (call_id, phone_number, transcript, summary, category)
                VALUES (?, ?, ?, ?, ?)
            """, (call_id, customer_phone, transcript, summary, category))
            db.commit()

            return {
                "status": "processed",
                "call_id": call_id,
                "category": category,
                "summary": summary
            }

        return {"status": "acknowledged", "type": message_type}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vapi Webhook Error: {str(e)}")
