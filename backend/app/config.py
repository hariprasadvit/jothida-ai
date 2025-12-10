"""
Configuration settings for ஜோதிட AI
"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    app_name: str = "ஜோதிட AI"
    debug: bool = True

    # Database - SQLite by default for easy local dev, PostgreSQL for production
    database_url: str = "sqlite:///./jothida_ai.db"

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"

    # JWT Settings
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Frontend URL
    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
