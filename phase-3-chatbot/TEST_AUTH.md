# Authentication Testing Guide

## Issues Fixed

### 1. Port Mismatch
- **Problem**: Frontend was configured for port 8002, but backend runs on port 8000
- **Fix**: Updated `frontend/.env.local` to use `http://localhost:8000`

### 2. Database Tables Not Created
- **Problem**: Conversation and Message models weren't registered in `models/__init__.py`
- **Fix**: Added imports for Conversation and Message models
- **Result**: All 4 tables now created: user, task, conversations, messages

### 3. Corrupted Backend .env File
- **Problem**: Duplicate text pasted at the end of the file
- **Fix**: Cleaned up the .env file to contain only valid configuration

## How to Test

### 1. Start Backend Server
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

### 3. Test Signup Flow
1. Open browser to `http://localhost:3000`
2. Click "Create Account"
3. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123!
4. Click "Sign up"
5. Should redirect to dashboard with authentication

### 4. Test Signin Flow
1. Go to `http://localhost:3000/auth/signin`
2. Enter credentials from signup
3. Click "Sign in"
4. Should redirect to dashboard

### 5. Verify Database
```bash
cd backend
python init_database.py
```

Should show all 4 tables created successfully.

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!","name":"Test User"}'
```

### Login User
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'
```

## Common Issues

### "Failed to fetch" Error
- **Cause**: Backend not running or wrong port
- **Solution**: Ensure backend is running on port 8000

### Tables Not Created
- **Cause**: Models not imported in `models/__init__.py`
- **Solution**: Run `python backend/init_database.py` to create tables

### CORS Errors
- **Cause**: Backend CORS not configured for frontend origin
- **Solution**: Backend already configured with `allow_origins=["*"]` for development

## Next Steps

After successful authentication:
1. Test task creation and management
2. Test AI chatbot functionality
3. Verify JWT token handling
4. Test logout functionality
