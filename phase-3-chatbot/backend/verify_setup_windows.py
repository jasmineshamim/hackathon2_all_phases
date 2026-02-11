"""
Windows-compatible backend testing guide for Phase III AI Chatbot.
"""
import sys
import os

print("=" * 70)
print("PHASE III BACKEND TESTING GUIDE")
print("=" * 70)

# Step 1: Check Python version
print("\n[STEP 1] Checking Python version...")
print("-" * 70)
python_version = sys.version_info
if python_version.major == 3 and python_version.minor >= 11:
    print(f"[OK] Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"[WARN] Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    print("       Recommended: Python 3.11+")

# Step 2: Check if dependencies are installed
print("\n[STEP 2] Checking required dependencies...")
print("-" * 70)

required_packages = {
    'fastapi': 'FastAPI web framework',
    'openai': 'OpenAI API client',
    'sqlmodel': 'SQLModel ORM',
    'uvicorn': 'ASGI server',
}

missing_packages = []
for package, description in required_packages.items():
    try:
        __import__(package)
        print(f"[OK] {package:15} - {description}")
    except ImportError:
        print(f"[FAIL] {package:15} - {description} (NOT INSTALLED)")
        missing_packages.append(package)

if missing_packages:
    print(f"\n[WARN] Missing {len(missing_packages)} required package(s)")
    print("\nTo install missing dependencies, run:")
    print("   cd backend")
    print("   pip install -r requirements.txt")
else:
    print(f"\n[OK] All required dependencies installed!")

# Step 3: Check environment variables
print("\n[STEP 3] Checking environment variables...")
print("-" * 70)
from dotenv import load_dotenv

load_dotenv('backend/.env')

env_vars = {
    'OPENAI_API_KEY': 'OpenAI API key for chat agent',
    'DATABASE_URL': 'Database connection string',
}

missing_env = []
for var, description in env_vars.items():
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if 'KEY' in var or 'SECRET' in var:
            display_value = value[:10] + '...' if len(value) > 10 else '***'
        else:
            display_value = value[:50] + '...' if len(value) > 50 else value
        print(f"[OK] {var:20} - {display_value}")
    else:
        print(f"[FAIL] {var:20} - NOT SET")
        missing_env.append(var)

if missing_env:
    print(f"\n[WARN] Missing {len(missing_env)} environment variable(s)")
    print("\nPlease check backend/.env file")

# Step 4: Test database connection
print("\n[STEP 4] Testing database connection...")
print("-" * 70)
try:
    sys.path.append('.')
    from backend.database.session import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("[OK] Database connection successful")
except Exception as e:
    print(f"[FAIL] Database connection failed: {e}")

# Summary
print("\n" + "=" * 70)
print("SETUP VERIFICATION COMPLETE")
print("=" * 70)
print("\nNext steps:")
print("1. If all checks passed, run: python backend/test_phase3_backend.py")
print("2. Start backend server: python -m uvicorn backend.main:app --reload --port 8001")
print("3. Test chat endpoint with curl or Postman")
print("=" * 70)
