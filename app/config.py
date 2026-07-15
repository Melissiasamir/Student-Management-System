"""
Application configuration.

Centralizes environment-driven settings so the rest of the codebase
never hardcodes connection strings or app metadata.
"""

import os
from functools import lru_cache


class Settings:
    """Application settings, sourced from environment variables with sane defaults."""

    PROJECT_NAME: str = "Student Management System API"
    PROJECT_VERSION: str = "2.0.0"
    PROJECT_DESCRIPTION: str = (
        "A RESTful API for managing student records, evolved from a "
        "CLI-based JSON application into a production-grade FastAPI service."
    )

    # SQLite database file lives at the project root by default.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./students.db"
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (avoids re-reading env vars repeatedly)."""
    return Settings()


settings = get_settings()
