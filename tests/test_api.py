from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_dispatch_event_endpoint():
    response = client.post("/api/v1/events/dispatch?event_type=LEAD_QUALIFIED&description=Lead%20scored%20HOT&payload_json=%7B%22score%22%3A85%7D")
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "LEAD_QUALIFIED"
    assert data["db_persisted"] is True

def test_inbound_sms_webhook():
    response = client.post("/api/v1/sms/webhook?from_number=%2B15550199&message_body=Is%20there%20any%20available%20rent%20unit%3F")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success", f"Webhook failed with error: {data.get('message')}"

def test_rbac_authorization_flow():
    # 1. Obtain token for tenant
    res_tenant = client.post("/api/v1/auth/token?username=john_tenant&role=tenant")
    assert res_tenant.status_code == 200
    tenant_token = res_tenant.json()["access_token"]

    # 2. Tenant attempts to access admin endpoint -> 403 Forbidden
    res_forbidden = client.get("/api/v1/admin/dashboard", headers={"Authorization": f"Bearer {tenant_token}"})
    assert res_forbidden.status_code == 403

    # 3. Obtain token for admin
    res_admin = client.post("/api/v1/auth/token?username=admin_user&role=admin")
    assert res_admin.status_code == 200
    admin_token = res_admin.json()["access_token"]

    # 4. Admin accesses admin endpoint -> 200 OK
    res_success = client.get("/api/v1/admin/dashboard", headers={"Authorization": f"Bearer {admin_token}"})
    assert res_success.status_code == 200
    assert res_success.json()["status"] == "success"

def test_billing_balance():
    res = client.get("/api/v1/billing/balance?tenant_id=t_123&base_rent=2000&days_late=6")
    assert res.status_code == 200
    assert res.json()["late_fee"] == 60.0

def test_work_order_creation():
    res = client.post("/api/v1/maintenance/work-orders?tenant_id=t_123&description=Leaking%20pipe&category=plumbing")
    assert res.status_code == 200
    assert res.json()["urgency"] == "HIGH"

def test_lead_scoring():
    res = client.post("/api/v1/leads/score?income=9000&rent=2500&credit_score=720")
    assert res.status_code == 200
    assert res.json()["qualification_tier"] == "HOT"

def test_billing_balance():
    res = client.get("/api/v1/billing/balance?tenant_id=t_123&base_rent=2000&days_late=6")
    assert res.status_code == 200
    assert res.json()["late_fee"] == 60.0

def test_work_order_creation():
    res = client.post("/api/v1/maintenance/work-orders?tenant_id=t_123&description=Leaking%20pipe&category=plumbing")
    assert res.status_code == 200
    assert res.json()["urgency"] == "HIGH"

def test_lead_scoring():
    res = client.post("/api/v1/leads/score?income=9000&rent=2500&credit_score=720")
    assert res.status_code == 200
    assert res.json()["qualification_tier"] == "HOT"

def test_lease_generation():
    res = client.post("/api/v1/leases/generate?tenant_name=Jane%20Doe&property_address=123%20Main%20St&monthly_rent=2000")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "DRAFT_PENDING_SIGNATURE"
    assert data["total_move_in_cost"] == 5000.0

def test_lease_execution():
    res = client.post("/api/v1/leases/sign?lease_id=lease_12345678&tenant_signature=Jane%20Doe")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "EXECUTED"
    assert data["onboarding_checklist"]["lease_signed"] is True

def test_vendor_job_assignment():
    res = client.post("/api/v1/vendors/jobs/assign?vendor_name=Apex%20Plumbing&work_order_id=wo_12345678&property_address=123%20Main%20St&estimated_cost=350")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "DISPATCHED"
    assert data["vendor_name"] == "Apex Plumbing"

def test_vendor_invoice_submission():
    res = client.post("/api/v1/vendors/invoices/submit?job_id=job_12345678&labor_cost=400&materials_cost=150")
    assert res.status_code == 200
    data = res.json()
    assert data["total_amount"] == 550.0
    assert data["status"] == "APPROVED_FOR_PAYMENT"

def test_payout_calculation():
    res = client.post("/api/v1/payouts/calculate?owner_id=o_123&property_address=123%20Main%20St&gross_rent_collected=3000&management_fee_pct=10&maintenance_expenses=200&reserve_holdback=250")
    assert res.status_code == 200
    data = res.json()
    assert data["management_fee"] == 300.0
    assert data["net_payout"] == 2250.0

def test_ach_batch_export():
    payout_data = [
        {"owner_id": "o_1", "net_payout": 2250.0},
        {"owner_id": "o_2", "net_payout": 1750.0}
    ]
    res = client.post("/api/v1/payouts/ach-batch", json=payout_data)
    assert res.status_code == 200
    data = res.json()
    assert data["total_records"] == 2
    assert data["total_batch_amount"] == 4000.0
    assert data["status"] == "READY_FOR_BANK_SUBMISSION"

def test_pdf_statement_generation():
    res = client.post("/api/v1/payouts/generate-pdf?owner_name=Apex%20Holdings&property_address=123%20Main%20St&gross_rent=3000")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "GENERATED"
    assert "PropFlow PM OS - Owner Distribution Statement" in data["html_document"]
    assert data["net_payout"] == 2450.0
