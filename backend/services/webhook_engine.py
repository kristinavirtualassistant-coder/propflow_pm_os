import urllib.request
import json
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook_engine")

# Global list of registered webhook endpoints
WEBHOOK_SUBSCRIBERS = [
    # Add external Make / Zapier / Vapi webhook URLs here
]

def dispatch_webhook_async(event_type: str, payload: dict):
    """Dispatches event payloads to all subscribers on a background thread."""
    def send_requests():
        event_data = {
            "event": event_type,
            "data": payload
        }
        json_data = json.dumps(event_data).encode("utf-8")

        for url in WEBHOOK_SUBSCRIBERS:
            try:
                req = urllib.request.Request(
                    url, 
                    data=json_data, 
                    headers={"Content-Type": "application/json", "User-Agent": "PropFlow-Webhook-Engine/1.0"}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    logger.info(f"✅ Webhook sent to {url} [Status: {response.status}]")
            except Exception as e:
                logger.error(f"❌ Failed to dispatch webhook to {url}: {e}")

    thread = threading.Thread(target=send_requests)
    thread.daemon = True
    thread.start()
