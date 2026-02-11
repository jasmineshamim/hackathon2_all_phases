"""Database migration framework initialization."""
from database.models.base import create_db_and_tables, engine
from sqlmodel import SQLModel
import logging

logger = logging.getLogger(__name__)


def run_migrations():
    """Run all database migrations."""
    try:
        logger.info("Starting database migrations...")
        create_db_and_tables()
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


def rollback_migrations():
    """Rollback database migrations (drop all tables)."""
    try:
        logger.warning("Rolling back database migrations...")
        SQLModel.metadata.drop_all(engine)
        logger.info("Database rollback completed")
    except Exception as e:
        logger.error(f"Rollback failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_migrations()
