import os
import json
import httpx
from typing import Dict, Any, Optional

VAPI_API_KEY = os.getenv("VAPI_API_KEY", "")
VAPI_BASE_URL = os.getenv("VAPI_BASE_URL", "https://api.vapi.ai")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

def calculate_lead_score(equity: str, property_type: str, phone: str) -> Dict[str, Any]:
    score = 50
    reasons = []

    if "$" in equity:
        try:
            val = float(equity.replace("$", "").replace(",", ""))
            if val >= 100000:
                score += 30
                reasons.append("High equity (>= $100k)")
            elif val >= 50000:
                score += 15
                reasons.append("Moderate equity (>= $50k)")
        except ValueError:
            pass

    if property_type.lower() in ["single family", "multi family", "duplex"]:
        score += 10
        reasons.append("Target residential asset class")

    if phone and len(phone) >= 10:
        score += 10
        reasons.append("Valid contact number available")

    tier = "HOT" if score >= 80 else "WARM" if score >= 60 else "COLD"
    return {"score": min(score, 100), "tier": tier, "reasons": reasons}

async def trigger_outbound_call(phone: str, lead_name: str, property_address: str) -> Dict[str, Any]:
    if not VAPI_API_KEY:
        return {
            "status": "SIMULATED",
            "call_id": "call_sim_9921",
            "message": "VAPI_API_KEY not configured. Simulated call triggered successfully.",
            "recipient": phone,
            "property": property_address
        }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{VAPI_BASE_URL}/call/phone",
                headers={
                    "Authorization": f"Bearer {VAPI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "phoneNumber": phone,
                    "assistant": {
                        "firstMessage": f"Hello {lead_name}, I'm calling from PropFlow Asset Management regarding your property at {property_address}. Are you open to a management proposal?",
                        "model": "gpt-4o"
                    }
                },
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}
