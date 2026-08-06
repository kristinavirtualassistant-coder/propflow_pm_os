import os
import sys
import sqlite3
import json
import uuid
from datetime import datetime

# Ensure project root is in PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import get_db_connection

class TelemetryLogger:
    """Logs system transactions, AI actions, and security access logs."""

    def __init__(self, organization_id: str = "org_pm_01"):
        self.organization_id = organization_id
        self._init_telemetry_table()

    def _init_telemetry_table(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id TEXT PRIMARY KEY,
            organization_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            details TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        conn.close()

    def log_event(self, event_type: str, actor_role: str, details: dict):
        conn = get_db_connection()
        cursor = conn.cursor()
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        cursor.execute("""
            INSERT INTO audit_logs (id, organization_id, event_type, actor_role, details)
            VALUES (?, ?, ?, ?, ?)
        """, (event_id, self.organization_id, event_type, actor_role, json.dumps(details)))
        conn.commit()
        conn.close()
        return event_id

    def get_recent_logs(self, limit: int = 5):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_logs WHERE organization_id = ? ORDER BY timestamp DESC LIMIT ?", (self.organization_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

if __name__ == "__main__":
    logger = TelemetryLogger()
    logger.log_event("PORTAL_ACCESS", "ADMIN", {"portal": "LEAD_GEN", "status": "SUCCESS"})
    print("[*] Recent Telemetry Logs:", logger.get_recent_logs(2))
