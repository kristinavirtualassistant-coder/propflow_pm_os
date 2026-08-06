import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "PropFlow PM OS"
    ENV: str = "development"
    DEBUG: bool = True
    
    # API Keys
    GEMINI_API_KEY: str = ""
    
    # Storage & Region Defaults
    DATABASE_URL: str = "sqlite:///./data/propflow_local.db"
    ORGANIZATION_ID: str = "org_pm_01"
    DEFAULT_COUNTRY: str = "US"
    DEFAULT_CITY: str = "Austin, TX"
    CURRENCY_SYMBOL: str = "$"

    # Portals Directory Matrix
    PORTALS: dict = {
        "LEAD_GEN": "LeadGen & Off-Market Deal Finder Portal",
        "PM_ADMIN": "Property Management Company Operations Portal",
        "OWNER": "Landlord & Owner Financial Portal",
        "TENANT": "Tenant Resident Portal",
        "VENDOR": "Maintenance & Contractor Portal"
    }

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

if __name__ == "__main__":
    print(f"[*] Configuration loaded for: {settings.APP_NAME}")
    print(f"[*] Default Region: {settings.DEFAULT_CITY}, {settings.DEFAULT_COUNTRY}")
