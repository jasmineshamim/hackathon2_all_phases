# Quickstart: Todo Full-Stack Web Application

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL client tools (for Neon connection)
- Git for version control

## Environment Setup

### 1. Clone and Initialize Repository
```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"
BETTER_AUTH_URL="http://localhost:3000"
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
```

## Database Setup

1. Create a Neon Serverless PostgreSQL database
2. Set the DATABASE_URL in backend .env file
3. Run database migrations:
```bash
cd backend
python -m database.migrate
```

## Running the Application

### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication (Better Auth)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Management (JWT Required)
- `GET /api/{user_id}/tasks` - List all user tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Development Workflow

1. Start backend server on port 8000
2. Start frontend server on port 3000
3. Access the application at http://localhost:3000
4. Register/login to create tasks
5. All API calls will automatically include JWT tokens

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Frontend
Deploy to Vercel or similar platform:
```bash
npm run build
```

### Backend
Deploy to Railway, Render, or similar platform with Python support.