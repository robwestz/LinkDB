"""
Configuration management for LinkDB backend.

This module handles all environment-based configuration using Pydantic Settings.
Secrets and environment-specific values should be stored in .env file.
"""

from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "LinkDB Analytics API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # Database
    DATABASE_URL: str = "sqlite:///./data/output/linkops_history.db"

    # Security
    SECRET_KEY: str = "CHANGE-THIS-IN-PRODUCTION-USE-STRONG-RANDOM-KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/linkdb.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Cache
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    CACHE_MAX_SIZE: int = 1000

    # Email (for scheduled reports)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@linkdb.com"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_database_path() -> Path:
    """Get absolute path to the database file."""
    # If DATABASE_URL is sqlite://, extract the path
    if settings.DATABASE_URL.startswith("sqlite:///"):
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        if db_path.startswith("./"):
            # Relative to project root
            return Path(__file__).parent.parent.parent / db_path.lstrip("./")
        return Path(db_path)
    raise ValueError(f"Unsupported DATABASE_URL format: {settings.DATABASE_URL}")


# Validate settings on import
def validate_settings():
    """Validate critical settings on startup."""
    errors = []

    # Check if secret key is changed in production
    if settings.ENVIRONMENT == "production" and "CHANGE-THIS" in settings.SECRET_KEY:
        errors.append("⚠️  SECRET_KEY must be changed in production!")

    # Check if allowed origins is set in production
    if settings.ENVIRONMENT == "production" and "localhost" in str(settings.ALLOWED_ORIGINS):
        errors.append("⚠️  ALLOWED_ORIGINS contains localhost in production!")

    # Check if debug is disabled in production
    if settings.ENVIRONMENT == "production" and settings.DEBUG:
        errors.append("⚠️  DEBUG should be False in production!")

    # Check if database path exists
    try:
        db_path = get_database_path()
        if not db_path.parent.exists():
            errors.append(f"⚠️  Database directory does not exist: {db_path.parent}")
    except Exception as e:
        errors.append(f"⚠️  Database path error: {e}")

    # Check SMTP config if email features are enabled
    if settings.SMTP_USER and not settings.SMTP_PASSWORD:
        errors.append("⚠️  SMTP_USER is set but SMTP_PASSWORD is missing!")

    if errors:
        print("🔧 Configuration Validation Warnings:")
        for error in errors:
            print(f"   {error}")
        print()

    return len(errors) == 0


# Run validation on import
validate_settings()
