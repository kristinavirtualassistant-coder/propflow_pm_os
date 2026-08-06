import sqlite3
import json
import os
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "propflow_local.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Instantiates relational tables for all 5 portals."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Organizations (Multi-Tenant Companies)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        plan_tier TEXT DEFAULT 'growth',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Users (RBAC)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        role TEXT NOT NULL, -- 'ADMIN', 'LANDLORD', 'TENANT', 'VENDOR'
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id)
    );
    """)

    # 3. Properties & Units
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        owner_id TEXT NOT NULL,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        property_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id),
        FOREIGN KEY (owner_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS units (
        id TEXT PRIMARY KEY,
        property_id TEXT NOT NULL,
        unit_number TEXT NOT NULL,
        market_rent REAL NOT NULL,
        status TEXT DEFAULT 'VACANT',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (property_id) REFERENCES properties(id)
    );
    """)

    # 4. Leases
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leases (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        unit_id TEXT NOT NULL,
        tenant_id TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        monthly_rent REAL NOT NULL,
        status TEXT DEFAULT 'ACTIVE',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id),
        FOREIGN KEY (unit_id) REFERENCES units(id),
        FOREIGN KEY (tenant_id) REFERENCES users(id)
    );
    """)

    # 5. Work Orders (Maintenance)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_orders (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        unit_id TEXT NOT NULL,
        tenant_id TEXT NOT NULL,
        vendor_id TEXT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        priority TEXT DEFAULT 'ROUTINE',
        status TEXT DEFAULT 'SUBMITTED',
        ai_diagnosis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id),
        FOREIGN KEY (unit_id) REFERENCES units(id)
    );
    """)

    # 6. PropStream-Style LeadGen Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prospect_properties (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        owner_name TEXT,
        owner_type TEXT DEFAULT 'INDIVIDUAL',
        estimated_equity REAL,
        distress_tags TEXT, -- JSON array
        status TEXT DEFAULT 'NEW',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organization_id) REFERENCES organizations(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skip_trace_records (
        id TEXT PRIMARY KEY,
        prospect_property_id TEXT NOT NULL,
        phone_numbers TEXT, -- JSON array
        email_addresses TEXT, -- JSON array
        traced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (prospect_property_id) REFERENCES prospect_properties(id)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("[*] PropFlow PM OS Database instantiated successfully.")
