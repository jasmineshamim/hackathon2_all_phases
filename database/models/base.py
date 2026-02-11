"""Database base configuration and connection setup."""
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool
import os
from typing import Generator

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create engine with Neon PostgreSQL optimizations
engine = create_engine(
    DATABASE_URL,
    echo=True if os.getenv("DEBUG", "False") == "True" else False,
    poolclass=NullPool,  # Neon handles connection pooling
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
    }
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session
