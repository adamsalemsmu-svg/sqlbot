"""
Database models and session factory.

This module centralises the SQLAlchemy declarations used across the
application.  It defines a simple ``Message`` model for logging chat
interactions and exposes ``engine`` and ``SessionLocal`` helpers based on
configuration from environment variables.
"""

from datetime import datetime
import os

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import Engine


# Load database URL from environment; default to SQLite in local file
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///conversations.db")

# Create the SQLAlchemy engine.  ``future=True`` enables SQLAlchemy 2.0 API.
engine: Engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,
)

# Declarative base class for model definitions
Base = declarative_base()

# Session factory bound to our engine
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


class Message(Base):
    """Represents a single chat message and response."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<Message id={self.id!r} user={self.user!r}"
            f" timestamp={self.timestamp.isoformat()}>"
        )