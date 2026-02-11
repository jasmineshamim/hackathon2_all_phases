# Complete Setup and Testing Guide

## Summary of Fixes Applied

### 1. **Port Configuration Fixed**
- **Issue**: Frontend was configured for port 8002, backend runs on port 8000
- **Fix**: Updated `frontend/.env.local` to use `http://localhost:8000`

### 2. **Database Tables Created**
- **Issue**: Conversation and Message models weren't registered
- **Fix**: Updated `backend/models/__init__.py` to include all models
- **Result**: All 4 tables created successfully:
  - `user` - User accounts
  - `task` - Todo tasks
  - `conversations` - AI chat conversations
  - `messages` - Chat messages

### 3. **Backend .env File Cleaned**
- **Issue**: Corrupted with duplicate text
- **Fix**: Cleaned up to contain only valid configuration

## Current Status

✅ Database tables created and verified
✅ Backend configuration fixed
✅ Frontend configuration fixed
✅ All models properly registered

## How to Start the Application

### Option 1: Using Batch Files (Windows)

**Start Backend:**
```cmd
start_backend.bat
```

**Start Frontend (in a new terminal):**
```cmd
start_frontend.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Testing the Application

### 1. Verify Backend is Running
Open browser to: `http://localhost:8000/docs`

You should see the Swagger UI with all API endpoints.

### 2. Test Authentication Flow

**A. Sign Up:**
1. Go to `http://localhost:3000`
2. Click "Create Account"
3. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123!
4. Click "Sign up"
5. Should redirect to `/dashboard` with authentication

**B. Sign In:**
1. Go to `http://localhost:3000/auth/signin`
2. Enter the credentials you created
3. Click "Sign in"
4. Should redirect to `/dashboard`

### 3. Test API Directly

Run the test script:
```bash
python test_backend_api.py
```

This will test:
- Health check endpoint
- Root endpoint
- Registration endpoint
- Login endpoint

## Troubleshooting

### "Failed to fetch" Error

**Symptoms:**
- Frontend shows "Error: Failed to fetch"
- Network tab shows failed requests

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend logs for errors
3. Ensure no firewall blocking port 8000
4. Verify `.env.local` has correct URL: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`

### Backend Not Starting

**Check if port 8000 is already in use:**
```bash
netstat -ano | findstr :8000
```

**If port is occupied, kill the process:**
```bash
# Find the PID from netstat output, then:
taskkill /PID <PID> /F
```

### Database Issues

**Recreate tables:**
```bash
cd backend
python init_database.py
```

**Verify tables exist:**
```bash
cd backend
python -c "from sqlalchemy import text; from database.session import engine; conn = engine.connect(); result = conn.execute(text('SELECT name FROM sqlite_master WHERE type=\"table\"')); print([r[0] for r in result])"
```

### CORS Errors

The backend is configured with `allow_origins=["*"]` for development, so CORS should not be an issue. If you still see CORS errors:

1. Check browser console for exact error
2. Verify backend CORS middleware is loaded
3. Restart both frontend and backend

## API Documentation

Once backend is running, access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./test.db
BETTER_AUTH_SECRET=test-secret-key-for-development
BETTER_AUTH_URL=http://localhost:3000
JWT_SECRET_KEY=test-secret-key-for-development
JWT_REFRESH_SECRET_KEY=test-secret-key-for-development
OPENAI_API_KEY=<your-key>
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=
```

## Next Steps After Successful Authentication

1. **Test Task Management**
   - Create tasks
   - Update tasks
   - Delete tasks
   - Mark tasks as complete

2. **Test AI Chatbot**
   - Access chatbot interface
   - Send messages
   - Verify conversation history

3. **Test Logout**
   - Click logout button
   - Verify tokens are cleared
   - Verify redirect to login page

## Production Considerations

Before deploying to production:

1. **Change all secrets** in `.env` files
2. **Update CORS settings** to allow only your frontend domain
3. **Use PostgreSQL** instead of SQLite (update DATABASE_URL)
4. **Enable HTTPS** for both frontend and backend
5. **Set up proper authentication** with email verification
6. **Add rate limiting** for API endpoints
7. **Set up monitoring** and logging
