import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PropFlow PM OS"
    ENV: str = "development"
    DEBUG: bool = True
    JWT_SECRET_KEY: str = "propflow_super_secret_jwt_key_2026"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./propflow.db"
    VAPI_API_KEY: str = ""
    VAPI_BASE_URL: str = "https://api.vapi.ai"
    MAKE_WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
