from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from datetime import datetime, timezone
from .database import init_db
from .routers import auth, items
from .config import settings
from .schemas import HealthCheck

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A lightweight FastAPI-inspired REST API framework with automatic validation, built-in security, and OpenAPI documentation.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure with your domain in production
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(items.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Python API Framework",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="ok",
        timestamp=datetime.now(timezone.utc),
        version="0.1.0"
    )

@app.get("/api/v1/health", response_model=HealthCheck, tags=["health"])
async def api_health_check():
    """API health check endpoint."""
    return HealthCheck(
        status="ok",
        timestamp=datetime.now(timezone.utc),
        version="0.1.0"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "py_api_framework.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 