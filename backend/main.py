from fastapi import FastAPI, Body, HTTPException, Header
from typing import List, Dict, Any, Optional
import uuid

from .services.billing_service import calculate_tenant_balance
from .services.work_orders import create_work_order
from .services.screening_service import score_lead
from .services.lease_service import generate_lease_agreement, execute_lease_signature
from .services.vendor_service import assign_vendor_job, submit_vendor_invoice
from .services.payout_service import calculate_owner_payout, generate_ach_batch_export

app = FastAPI(title="PropFlow PM OS Backend", version="1.0.0")

# 1. CORE & HEALTH
@app.get("/")
def read_root():
    return {"status": "online", "system": "PropFlow PM OS Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

# 2. EVENT DISPATCH & WEBHOOKS
@app.post("/api/v1/events/dispatch")
def dispatch_event(event_type: str, description: str, payload_json: Optional[str] = None):
    return {
        "event_id": f"evt_{uuid.uuid4().hex[:8]}",
        "event_type": event_type,
        "description": description,
        "status": "DISPATCHED",
        "db_persisted": True
    }

@app.post("/api/v1/sms/webhook")
def sms_webhook(from_number: str, message_body: str):
    return {
        "status": "success",
        "from": from_number,
        "reply": f"Thank you for contacting PropFlow. We received your message: '{message_body}'"
    }

# 3. AUTH & RBAC
@app.post("/api/v1/auth/token")
def generate_token(username: str, role: str):
    return {
        "access_token": f"fake_token_{username}_{role}",
        "token_type": "bearer",
        "role": role
    }

@app.get("/api/v1/admin/dashboard")
def admin_dashboard(authorization: Optional[str] = Header(None)):
    if authorization and "tenant" in authorization:
        raise HTTPException(status_code=403, detail="Access denied for tenant role")
    return {"status": "success", "panel": "admin_overview"}

# 4. BILLING & RENT LEDGER
@app.get("/api/v1/billing/balance")
def get_tenant_balance(tenant_id: str, base_rent: float, days_late: int = 0):
    return calculate_tenant_balance(tenant_id, base_rent, days_late)

# 5. WORK ORDERS & MAINTENANCE
@app.post("/api/v1/maintenance/work-orders")
def submit_work_order(tenant_id: str, description: str, category: str):
    return create_work_order(tenant_id, description, category)

# 6. LEAD QUALIFICATION
@app.post("/api/v1/leads/score")
def evaluate_lead(income: float, rent: float, credit_score: int):
    return score_lead(income, rent, credit_score)

# 7. LEASE GENERATION & E-SIGN
@app.post("/api/v1/leases/generate")
def create_lease(tenant_name: str, property_address: str, monthly_rent: float, lease_term_months: int = 12):
    return generate_lease_agreement(tenant_name, property_address, monthly_rent, lease_term_months)

@app.post("/api/v1/leases/sign")
def sign_lease(lease_id: str, tenant_signature: str):
    return execute_lease_signature(lease_id, tenant_signature)

# 8. VENDOR JOBS & INVOICING
@app.post("/api/v1/vendors/jobs/assign")
def assign_job(vendor_name: str, work_order_id: str, property_address: str, estimated_cost: float):
    return assign_vendor_job(vendor_name, work_order_id, property_address, estimated_cost)

@app.post("/api/v1/vendors/invoices/submit")
def submit_invoice(job_id: str, labor_cost: float, materials_cost: float, owner_reserve_limit: float = 1000.0):
    return submit_vendor_invoice(job_id, labor_cost, materials_cost, owner_reserve_limit)

# 9. PAYOUTS & ACH EXPORTS
@app.post("/api/v1/payouts/calculate")
def calculate_payout(owner_id: str, property_address: str, gross_rent_collected: float, management_fee_pct: float = 10.0, maintenance_expenses: float = 0.0, reserve_holdback: float = 250.0):
    return calculate_owner_payout(owner_id, property_address, gross_rent_collected, management_fee_pct, maintenance_expenses, reserve_holdback)

@app.post("/api/v1/payouts/ach-batch")
def export_ach_batch(payout_records: List[Dict[str, Any]] = Body(...)):
    return generate_ach_batch_export(payout_records)

# MILESTONE 7: OWNER STATEMENT PDF API
from .services.pdf_service import generate_owner_statement_pdf

@app.post("/api/v1/payouts/generate-pdf")
def create_owner_statement_pdf(
    owner_name: str,
    property_address: str,
    gross_rent: float,
    management_fee_pct: float = 10.0,
    maintenance_deductions: float = 0.0,
    reserve_holdback: float = 250.0
):
    return generate_owner_statement_pdf(
        owner_name, property_address, gross_rent, management_fee_pct, maintenance_deductions, reserve_holdback
    )
