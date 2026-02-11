"""FastAPI main application with CORS configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from database.models.base import create_db_and_tables
from backend.src.api import todos, chat, mcp_tools, health
from backend.src.middleware.rate_limit import rate_limit_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Todo Chatbot API",
    description="AI-Powered Todo Chatbot with MCP Tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(todos.router, prefix="/api/v1/todos", tags=["todos"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(mcp_tools.router, prefix="/api/v1/mcp", tags=["mcp-tools"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Starting Todo Chatbot API...")
    try:
        create_db_and_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Todo Chatbot API...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

