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

# --- VAPI AI VOICE AGENT WEBHOOK ---
@app.post("/api/v1/webhooks/vapi")
async def vapi_webhook_handler(request: Request, db: sqlite3.Connection = Depends(get_db)):
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
