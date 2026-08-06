import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT", GMAIL_USER)

def send_google_email_alert(subject: str, body: str):
    """Sends an automated email dispatch via Gmail SMTP."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("⚠️ [GOOGLE DISPATCH MOCK] Email notification triggered:")
        print(f"   Subject: {subject}")
        print(f"   Body:\n{body}\n")
        return False

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = ALERT_RECIPIENT

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Google Email alert dispatched successfully to {ALERT_RECIPIENT}!")
        return True
    except Exception as e:
        print(f"❌ Failed to send Google Email alert: {e}")
        return False
