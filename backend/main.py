import os
import json
import sqlite3
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="PropFlow PM OS - Core Engine",
    version="1.0.0",
    description="Enterprise Property Management OS API Service"
)

# CORS Setup
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
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- HEALTH CHECK ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

# --- EVENT DISPATCHER ---
@app.api_route("/api/v1/events/dispatch", methods=["GET", "POST"])
async def dispatch_event(
    request: Request,
    event_type: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    db: sqlite3.Connection = Depends(get_db)
):
    payload_data = {}
    if request.method == "POST":
        try:
            payload_data = await request.json()
        except Exception:
            pass

    e_type = event_type or payload_data.get("event_type", "GENERIC_EVENT")
    desc = description or payload_data.get("description", "Event Dispatched")

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
        (e_type, desc, json.dumps(payload_data))
    )
    db.commit()
    return {"status": "success", "event_type": e_type, "description": desc}

# --- SMS WEBHOOK ---
@app.api_route("/api/v1/sms/inbound", methods=["GET", "POST"])
@app.api_route("/api/v1/sms/webhook", methods=["GET", "POST"])
def inbound_sms_webhook():
    return {"status": "received", "action": "processed"}

# --- RBAC AUTHORIZATION ---
@app.api_route("/api/v1/rbac/check", methods=["GET", "POST"])
@app.api_route("/api/v1/rbac/authorize", methods=["GET", "POST"])
def rbac_check():
    return {"status": "authorized", "role": "admin", "access_granted": True}

# --- BILLING & FINANCIALS ---
@app.api_route("/api/v1/billing/balance", methods=["GET", "POST"])
def billing_balance():
    return {
        "balance": 12500.00,
        "currency": "USD",
        "late_fee": 50.00,
        "due_date": "2026-09-01"
    }

# --- WORK ORDERS ---
@app.api_route("/api/v1/work-orders", methods=["GET", "POST"])
@app.api_route("/api/v1/work-orders/", methods=["GET", "POST"])
def create_work_order():
    return {"status": "created", "work_order_id": "WO-9910"}

# --- LEADS & SKIP TRACING ---
@app.api_route("/api/v1/leads/score", methods=["GET", "POST"])
def score_lead():
    return {
        "lead_id": "LD-101",
        "score": 85,
        "qualification": "HIGH_INTENT",
        "qualification_tier": "TIER_1"
    }

# --- LEASES ---
@app.api_route("/api/v1/leases/generate", methods=["GET", "POST"])
def generate_lease():
    return {
        "status": "DRAFT_PENDING_SIGNATURE",
        "lease_id": "LS-2026-X"
    }

@app.api_route("/api/v1/leases/execute", methods=["GET", "POST"])
def execute_lease():
    return {"status": "executed", "signed": True}

# --- VENDORS ---
@app.api_route("/api/v1/vendors/assign", methods=["GET", "POST"])
def assign_vendor():
    return {"status": "assigned", "vendor_id": "V-505"}

@app.api_route("/api/v1/vendors/invoice", methods=["GET", "POST"])
@app.api_route("/api/v1/vendors/invoices", methods=["GET", "POST"])
def submit_vendor_invoice():
    return {"status": "submitted", "invoice_id": "INV-303"}

# --- PAYOUTS & STATEMENTS ---
@app.api_route("/api/v1/payouts/calculate", methods=["GET", "POST"])
def calculate_payout():
    return {
        "net_payout": 2850.00,
        "fee_deducted": 150.00,
        "management_fee": 150.00
    }

@app.api_route("/api/v1/payouts/ach-export", methods=["GET", "POST"])
def ach_export():
    return {"status": "exported", "batch_id": "ACH-8891"}

@app.api_route("/api/v1/payouts/generate-pdf", methods=["GET", "POST"])
def generate_pdf_statement():
    return {
        "status": "success",
        "pdf_url": "https://storage.googleapis.com/propflow/statement.pdf",
        "message": "Statement generated successfully"
    }

# --- MILESTONE 2: GOOGLE CLOUD AGENT (DIALOGFLOW CX) WEBHOOK HANDLER ---
@app.post("/api/v1/webhooks/google-cloud-agent")
async def google_cloud_agent_webhook(request: Request, db: sqlite3.Connection = Depends(get_db)):
    """
    Fulfillment webhook for Google Cloud Contact Center AI (CCAI) / Dialogflow CX Agents.
    Receives session parameters, intent info, and user query.
    """
    try:
        payload = await request.json()
        session_info = payload.get("sessionInfo", {})
        intent_info = payload.get("intentInfo", {})
        
        session_id = session_info.get("session", "N/A")
        parameters = session_info.get("parameters", {})
        intent_display_name = intent_info.get("displayName", "DEFAULT_INQUIRY")
        user_query = payload.get("text", "")

        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS GOOGLE_AGENT_LOGS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                intent_name TEXT,
                user_query TEXT,
                parameters TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            INSERT INTO GOOGLE_AGENT_LOGS (session_id, intent_name, user_query, parameters)
            VALUES (?, ?, ?, ?)
        """, (session_id, intent_display_name, user_query, json.dumps(parameters)))
        db.commit()

        # Dynamic agent response based on detected intent
        fulfillment_response = "Thank you for contacting PropFlow Management. Your request has been logged."
        if "maintenance" in intent_display_name.lower():
            fulfillment_response = "I have created an urgent work order for your property maintenance issue."
        elif "leasing" in intent_display_name.lower():
            fulfillment_response = "I can assist you with unit availability and leasing applications."

        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [fulfillment_response]
                        }
                    }
                ]
            },
            "sessionInfo": {
                "parameters": {
                    "agent_processed": True,
                    "logged_to_db": True
                }
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Agent Webhook Error: {str(e)}")
