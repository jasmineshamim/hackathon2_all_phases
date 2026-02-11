"""Database migration for todos table."""
from sqlmodel import SQLModel, create_engine
from database.models.base import engine
from database.models.todo import Todo
from database.models.user import User
import logging

logger = logging.getLogger(__name__)


def upgrade():
    """Create todos table with indexes."""
    try:
        logger.info("Creating todos table...")

        # Import models to ensure they're registered
        from database.models.todo import Todo
        from database.models.user import User

        # Create tables
        SQLModel.metadata.create_all(engine, tables=[Todo.__table__])

        logger.info("Todos table created successfully")

        # Note: Indexes are automatically created by SQLModel based on Field(index=True)
        # Additional indexes:
        # - user_id (already indexed via Field definition)
        # - user_id + status (composite index for filtered queries)
        # - user_id + priority (composite index for priority sorting)
        # - user_id + due_date (composite index for deadline queries)

    except Exception as e:
        logger.error(f"Failed to create todos table: {str(e)}")
        raise


def downgrade():
    """Drop todos table."""
    try:
        logger.info("Dropping todos table...")
        SQLModel.metadata.drop_all(engine, tables=[Todo.__table__])
        logger.info("Todos table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop todos table: {str(e)}")
        raise


if __name__ == "__main__":
    upgrade()
