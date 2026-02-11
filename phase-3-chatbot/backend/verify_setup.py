"""
Step-by-step backend testing guide for Phase III AI Chatbot.
Run this script to verify your backend foundation is working.
"""
import sys
import subprocess

print("=" * 70)
print("PHASE III BACKEND TESTING GUIDE")
print("=" * 70)

# Step 1: Check Python version
print("\n[STEP 1] Checking Python version...")
print("-" * 70)
python_version = sys.version_info
if python_version.major == 3 and python_version.minor >= 11:
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"⚠️  Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    print("   Recommended: Python 3.11+")

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
        print(f"✅ {package:15} - {description}")
    except ImportError:
        print(f"❌ {package:15} - {description} (NOT INSTALLED)")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️  Missing {len(missing_packages)} required package(s)")
    print("\nTo install missing dependencies, run:")
    print("   cd backend")
    print("   pip install -r requirements.txt")
    print("\nOr install individually:")
    for pkg in missing_packages:
        print(f"   pip install {pkg}")
    sys.exit(1)
else:
    print(f"\n✅ All required dependencies installed!")

# Step 3: Check environment variables
print("\n[STEP 3] Checking environment variables...")
print("-" * 70)
import os
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
        print(f"✅ {var:20} - {display_value}")
    else:
        print(f"❌ {var:20} - NOT SET")
        missing_env.append(var)

if missing_env:
    print(f"\n⚠️  Missing {len(missing_env)} environment variable(s)")
    print("\nPlease set in backend/.env:")
    for var in missing_env:
        print(f"   {var}=your_value_here")
    sys.exit(1)

# Step 4: Test database connection
print("\n[STEP 4] Testing database connection...")
print("-" * 70)
try:
    sys.path.append('.')
    from backend.database.session import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)

# Step 5: Instructions for running tests
print("\n[STEP 5] Ready to run comprehensive tests")
print("-" * 70)
print("✅ All prerequisites met!")
print("\nNext steps:")
print("\n1. Run comprehensive backend tests:")
print("   python backend/test_phase3_backend.py")
print("\n2. Start the backend server:")
print("   cd backend")
print("   python -m uvicorn main:app --reload --port 8001")
print("\n3. Test the chat endpoint:")
print("   curl -X POST http://localhost:8001/api/test_user/chat \\")
print("        -H 'Content-Type: application/json' \\")
print("        -H 'Authorization: Bearer test_token' \\")
print("        -d '{\"message\": \"Add a task to buy groceries\"}'")
print("\n4. Once backend is verified, proceed with Phase 3 (Frontend)")

print("\n" + "=" * 70)
print("SETUP VERIFICATION COMPLETE")
print("=" * 70)
