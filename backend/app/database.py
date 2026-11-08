"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Database engine, session factory, and base model declaration.
Supports PostgreSQL (production) with automatic SQLite fallback for local testing.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

# Connect args needed for SQLite thread compatibility; empty for PostgreSQL
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency to yield database session and ensure clean closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
