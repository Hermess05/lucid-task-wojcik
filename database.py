"""
This module sets up the database connection and session management for the application using SQLAlchemy.

It provides:
- `engine`: The SQLAlchemy engine for connecting to the database.
- `SessionLocal`: The session factory used to create database sessions.
- `Base`: The base class for SQLAlchemy models, which is used for declarative class definitions.

Configurations:
- `DATABASE_URL`: The connection string for the database (SQLite in this case).
- The `SessionLocal` factory will create sessions that do not autocommit or auto flush, giving more control over transactions.
- The `Base` class will be used to define ORM models, linking them to the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy engine for database connection
engine = create_engine(DATABASE_URL)

# SessionLocal is a session factory used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating SQLAlchemy ORM models
Base = declarative_base()
