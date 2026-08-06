from datetime import datetime, timezone
from typing import Dict, Any
import uuid

def generate_owner_statement_pdf(
    owner_name: str,
    property_address: str,
    gross_rent: float,
    management_fee_pct: float = 10.0,
    maintenance_deductions: float = 0.0,
    reserve_holdback: float = 250.0
) -> Dict[str, Any]:
    statement_id = f"pdf_stmt_{uuid.uuid4().hex[:8]}"
    management_fee = gross_rent * (management_fee_pct / 100.0)
    net_payout = gross_rent - management_fee - maintenance_deductions - reserve_holdback
    if net_payout < 0:
        net_payout = 0.0

    timestamp = datetime.now(timezone.utc).strftime("%B %Y")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #1e293b; }}
            .header {{ border-b: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 30px; }}
            .title {{ font-size: 24px; font-weight: bold; color: #0f172a; }}
            .subtitle {{ font-size: 14px; color: #64748b; margin-top: 5px; }}
            .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            .table th {{ background-color: #f8fafc; font-size: 12px; text-transform: uppercase; color: #64748b; }}
            .total-row {{ font-weight: bold; background-color: #f1f5f9; }}
            .net-amount {{ color: #10b981; font-size: 18px; font-weight: bold; }}
            .footer {{ margin-top: 40px; font-size: 11px; color: #94a3b8; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">PropFlow PM OS - Owner Distribution Statement</div>
            <div class="subtitle">Statement Period: {timestamp} | ID: {statement_id}</div>
        </div>
        
        <div>
            <p><strong>Owner:</strong> {owner_name}</p>
            <p><strong>Property Address:</strong> {property_address}</p>
        </div>

        <table class="table">
            <thead>
                <tr>
                    <th>Line Item Description</th>
                    <th style="text-align: right;">Amount ($)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Gross Rent Collected</td>
                    <td style="text-align: right;">${gross_rent:,.2f}</td>
                </tr>
                <tr>
                    <td>Management Fee ({management_fee_pct}%)</td>
                    <td style="text-align: right; color: #ef4444;">-${management_fee:,.2f}</td>
                </tr>
                <tr>
                    <td>Maintenance Expenses</td>
                    <td style="text-align: right; color: #ef4444;">-${maintenance_deductions:,.2f}</td>
                </tr>
                <tr>
                    <td>Reserve Holdback Escrow</td>
                    <td style="text-align: right; color: #f59e0b;">-${reserve_holdback:,.2f}</td>
                </tr>
                <tr class="total-row">
                    <td>Net Owner Distribution Payout</td>
                    <td style="text-align: right;" class="net-amount">${net_payout:,.2f}</td>
                </tr>
            </tbody>
        </table>

        <div class="footer">
            PropFlow Enterprise Property Automation System &bull; Direct Deposit ACH Wire Verification
        </div>
    </body>
    </html>
    """

    return {
        "statement_id": statement_id,
        "owner_name": owner_name,
        "property_address": property_address,
        "period": timestamp,
        "gross_rent": gross_rent,
        "net_payout": net_payout,
        "html_document": html_content.strip(),
        "download_url": f"/api/v1/payouts/pdf/{statement_id}",
        "status": "GENERATED"
    }
