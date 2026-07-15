"""
Database engine, session factory, and declarative base.

This module is the single source of truth for how the application
talks to SQLite through SQLAlchemy.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# `check_same_thread` is only required for SQLite, since FastAPI may
# handle a request in a different thread than the one that created
# the connection.
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and guarantees cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
