"""
Database initialization script.
Run this to create all database tables.
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.init_db import create_db_and_tables, check_db_connection
from models import User, Task, Conversation, Message

def main():
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)

    # Import all models to ensure they're registered
    print("\n1. Checking model imports...")
    print(f"   [OK] User model: {User}")
    print(f"   [OK] Task model: {Task}")
    print(f"   [OK] Conversation model: {Conversation}")
    print(f"   [OK] Message model: {Message}")

    # Create tables
    print("\n2. Creating database tables...")
    try:
        create_db_and_tables()
        print("   [OK] Database tables created successfully!")
    except Exception as e:
        print(f"   [ERROR] Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Verify tables exist
    print("\n3. Verifying tables...")
    try:
        tables = check_db_connection()
        print(f"   [OK] Found {len(tables)} tables: {', '.join(tables)}")

        # Check for expected tables
        expected_tables = ['user', 'task', 'conversations', 'messages']
        missing_tables = [t for t in expected_tables if t not in tables]

        if missing_tables:
            print(f"   [WARNING] Missing tables: {', '.join(missing_tables)}")
        else:
            print("   [OK] All expected tables exist!")

    except Exception as e:
        print(f"   [ERROR] Error checking tables: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
