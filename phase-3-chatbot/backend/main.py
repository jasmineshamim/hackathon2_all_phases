from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from dotenv import load_dotenv

import sys
import os
# Add the parent directory to the path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import database and middleware directly
from database.init_db import create_db_and_tables
from middleware.security import SecurityHeadersMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    logger.info("Initializing database tables...")
    create_db_and_tables()
    logger.info("Database tables initialized!")
    yield
    # Cleanup on shutdown if needed
    logger.info("Shutting down...")


from fastapi.security import HTTPBearer

# Initialize security scheme for Swagger UI
security_scheme = HTTPBearer()

app = FastAPI(
    lifespan=lifespan,
    title="Todo API",
    description="Secure Todo application API with JWT authentication",
    version="1.0.0",
    docs_url="/docs",  # Enable Swagger UI documentation
    redoc_url="/redoc",  # Enable ReDoc documentation
    # Add security scheme for API docs
    root_path=""  # This helps with reverse proxy setups
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware - add after security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes - import routers directly to avoid package issues
from routes.auth import router as auth_router
from routes.tasks import router as tasks_router

# Import chat router with error handling
import sys
try:
    from src.api.routes.chat import router as chat_router
    sys.stderr.write(f"[MAIN] Chat router imported successfully with {len(chat_router.routes)} routes\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MAIN] Failed to import chat router: {e}\n")
    sys.stderr.flush()
    import traceback
    traceback.print_exc()
    chat_router = None

# Include authentication routes without the /api prefix to match standard auth endpoints
app.include_router(auth_router)
# Include tasks routes without the /api prefix to match /tasks/ endpoint
app.include_router(tasks_router)
# Include chat routes for AI chatbot (Phase III)
if chat_router:
    app.include_router(chat_router)
    sys.stderr.write(f"[MAIN] Chat router included in app\n")
    sys.stderr.flush()
    # Force OpenAPI schema regeneration
    app.openapi_schema = None
else:
    sys.stderr.write("[MAIN] Chat router not included - import failed\n")
    sys.stderr.flush()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API", "status": "running"}

@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "healthy", "message": "API is running"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)