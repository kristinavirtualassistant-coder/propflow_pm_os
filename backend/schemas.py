from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class LeadCreate(BaseModel):
    address: str
    city: Optional[str] = "Austin"
    owner: Optional[str] = "Unknown"
    type: Optional[str] = "Single Family"
    equity: Optional[str] = "$0"
    tags: Optional[List[str]] = []
    phones: Optional[List[str]] = []

class LeadResponse(LeadCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class WorkOrderCreate(BaseModel):
    property_address: str
    title: str
    unit: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = "MEDIUM"

class WorkOrderStatusUpdate(BaseModel):
    status: str

class WorkOrderResponse(WorkOrderCreate):
    id: str
    status: Optional[str] = "OPEN"
    created_at: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class FinancialRecordCreate(BaseModel):
    owner_name: str
    property_address: str
    gross_rent: float
    management_fee_pct: Optional[float] = 0.10
    reserve_fund_pct: Optional[float] = 0.05
    maintenance_deductions: Optional[float] = 0.0
    month_year: Optional[str] = "2026-08"

class FinancialRecordResponse(FinancialRecordCreate):
    id: str
    management_fee_amount: Optional[float] = 0.0
    reserve_fund_amount: Optional[float] = 0.0
    net_distribution: Optional[float] = 0.0
    model_config = ConfigDict(from_attributes=True)
