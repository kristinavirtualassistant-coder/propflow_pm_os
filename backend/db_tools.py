import os
import sys
import json
import sqlite3
from datetime import datetime

# Check root directory or backend directory for propflow.db
if os.path.exists("propflow.db"):
    DB_PATH = "propflow.db"
elif os.path.exists("backend/propflow.db"):
    DB_PATH = "backend/propflow.db"
else:
    DB_PATH = "propflow.db"

def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"⚠️ Database file '{DB_PATH}' does not exist yet.")
        print("💡 Ensure uvicorn backend.main:app is running to create database tables.")
        sys.exit(1)
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database {DB_PATH}: {e}")
        sys.exit(1)

def inspect_db():
    """Prints table schema and current row counts."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()

    print("\n" + "=" * 50)
    print(f"📊 PROPFLOW PM OS - DATABASE INSPECTION ({DB_PATH})")
    print("=" * 50)

    if not tables:
        print("⚠️ No tables found in database.")
        print("💡 Make sure FastAPI is running (uvicorn backend.main:app --reload) to trigger startup seed data.")
        return

    for table in tables:
        table_name = table["name"]
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name};")
        row_count = cursor.fetchone()["count"]

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        col_names = [f"{col['name']} ({col['type']})" for col in columns]

        print(f"\n📂 Table: {table_name.upper()} ({row_count} rows)")
        print(f"   Columns: {', '.join(col_names)}")

    print("\n" + "=" * 50 + "\n")
    conn.close()

def export_json():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()

    export_data = {}

    for table in tables:
        table_name = table["name"]
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        export_data[table_name] = []
        for row in rows:
            row_dict = dict(row)
            for k, v in row_dict.items():
                if isinstance(v, str) and (v.startswith("[") or v.startswith("{")):
                    try:
                        row_dict[k] = json.loads(v)
                    except json.JSONDecodeError:
                        pass
            export_data[table_name].append(row_dict)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_propflow_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Successfully exported JSON database backup to: {filename}")
    conn.close()

def export_sql_dump():
    conn = connect_db()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_propflow_{timestamp}.sql"

    with open(filename, "w") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")

    print(f"✅ Successfully exported SQL dump file to: {filename}")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python3 backend/db_tools.py inspect  -> View tables, columns, and row counts")
        print("  python3 backend/db_tools.py json     -> Export full database to JSON")
        print("  python3 backend/db_tools.py sql      -> Export raw SQL dump file\n")
        sys.exit(0)

    action = sys.argv[1].lower()

    if action == "inspect":
        inspect_db()
    elif action == "json":
        export_json()
    elif action == "sql":
        export_sql_dump()
    else:
        print(f"Unknown command: {action}")
