from sqlmodel import SQLModel
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import engine
from models.user import User
from models.task import Task
from models.conversation import Conversation
from models.message import Message


def create_db_and_tables():
    """
    Create database tables using SQLModel metadata.
    This function ensures all tables defined in the models are created.
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


async def create_db_and_tables_async():
    """
    Async version of table creation - useful for lifespan events.
    """
    print("Creating database tables asynchronously...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


def check_db_connection():
    """
    Test database connection and list existing tables.
    """
    from sqlalchemy import text
    from config.settings import settings

    with engine.connect() as connection:
        DATABASE_URL = settings.DATABASE_URL

        if 'sqlite' in DATABASE_URL:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
        else:
            result = connection.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            )
            tables = [row[0] for row in result.fetchall()]

        print(f"Existing tables in database: {tables}")
        return tables