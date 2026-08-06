import sqlite3
import urllib.request
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "propflow.db")

def run_diagnostics():
    print("\n🔍 --- PROPFLOW PM OS AUTOMATED DIAGNOSTICS --- 🔍")
    
    # Check DB
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"✅ Database File: OK ({len(tables)} active tables: {', '.join(tables)})")
        conn.close()
    else:
        print("❌ Database File: MISSING")

    # Check API Health
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=3) as resp:
            data = json.loads(resp.read().decode())
            print(f"✅ FastAPI Backend: HEALTHY (Status: {data.get('status')})")
    except Exception as e:
        print(f"❌ FastAPI Backend: UNHEALTHY ({e})")

    print("------------------------------------------------\n")

if __name__ == "__main__":
    run_diagnostics()
