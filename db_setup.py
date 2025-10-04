"""
Database setup script.

Run this script once to create the database tables for SQLBot.  It uses
the settings from ``models.py``, including the ``DATABASE_URL``
environment variable.  If the database does not exist it will be
created automatically when using SQLite.  For Postgres or other
engines, ensure the target database has already been created.

Usage::

    python db_setup.py

"""

from models import Base, engine


def create_tables() -> None:
    """Create all tables defined on the declarative base."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")