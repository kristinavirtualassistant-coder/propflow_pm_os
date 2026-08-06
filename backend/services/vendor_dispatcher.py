import uuid
from sqlalchemy.orm import Session
from backend.models import VendorModel

# Initial seed list of contractors
DEFAULT_VENDORS = [
    {"name": "Apex Plumbing Services", "trade": "PLUMBING", "phone": "+15125550101", "email": "dispatch@apexplumbing.com"},
    {"name": "Lone Star HVAC & Cooling", "trade": "HVAC", "phone": "+15125550102", "email": "service@lonestarhvac.com"},
    {"name": "VoltCraft Electrical", "trade": "ELECTRICAL", "phone": "+15125550103", "email": "jobs@voltcraftelectrical.com"},
    {"name": "Austin General Contractors", "trade": "GENERAL", "phone": "+15125550104", "email": "contact@austincm.com"},
]

def seed_vendors_if_empty(db: Session):
    """Ensures base vendor roster exists in database."""
    if db.query(VendorModel).count() == 0:
        for v in DEFAULT_VENDORS:
            db_vendor = VendorModel(id=f"vnd_{uuid.uuid4().hex[:6]}", **v)
            db.add(db_vendor)
        db.commit()

def auto_assign_vendor(title: str, description: str, db: Session):
    """Matches keywords to trade categories and assigns an active contractor."""
    seed_vendors_if_empty(db)
    
    content = f"{title} {description}".upper()
    
    trade = "GENERAL"
    if any(k in content for k in ["PIPE", "LEAK", "WATER", "PLUMB", "DRAIN", "SINK", "TOILET"]):
        trade = "PLUMBING"
    elif any(k in content for k in ["HVAC", "AC", "COOLING", "HEAT", "AIR", "THERMOSTAT"]):
        trade = "HVAC"
    elif any(k in content for k in ["WIRE", "POWER", "OUTLET", "BREAKER", "LIGHT", "ELECTR"]):
        trade = "ELECTRICAL"

    assigned_vendor = db.query(VendorModel).filter(
        VendorModel.trade == trade, 
        VendorModel.active == True
    ).first()

    if not assigned_vendor:
        assigned_vendor = db.query(VendorModel).filter(VendorModel.trade == "GENERAL").first()

    return assigned_vendor
