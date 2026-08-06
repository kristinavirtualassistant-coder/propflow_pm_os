from sqlalchemy import Column, String, Float, JSON, Boolean, Text
from backend.database import Base

class LeadModel(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    type = Column(String, nullable=False)
    equity = Column(String, nullable=False)
    tags = Column(JSON, default=list)
    phones = Column(JSON, default=list)

class WorkOrderModel(Base):
    __tablename__ = "work_orders"

    id = Column(String, primary_key=True)
    property_address = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="MEDIUM")
    status = Column(String, default="OPEN")
    created_at = Column(String, nullable=True)

class FinancialRecordModel(Base):
    __tablename__ = "financial_records"

    id = Column(String, primary_key=True)
    owner_name = Column(String, nullable=False)
    property_address = Column(String, nullable=False)
    gross_rent = Column(Float, nullable=False)
    management_fee_pct = Column(Float, nullable=False)
    reserve_fund_pct = Column(Float, nullable=False)
    maintenance_deductions = Column(Float, default=0.0)
    month_year = Column(String, nullable=False)

class VendorModel(Base):
    __tablename__ = "vendors"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    trade = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    active = Column(Boolean, default=True)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    event_type = Column(String, index=True)
    description = Column(Text)
    timestamp = Column(String)
    payload = Column(JSON, nullable=True)
