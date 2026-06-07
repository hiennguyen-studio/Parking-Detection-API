"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from pathlib import Path

from src.config.settings import settings
from src.config.logging_config import setup_logging
from src.backend.api.routes import (
    violations_router,
    cameras_router,
    users_router,
    statistics_router
)

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for dashboard
static_dir = Path(__file__).parent / "dashboard" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(violations_router)
app.include_router(cameras_router)
app.include_router(users_router)
app.include_router(statistics_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Illegal Parking Detection System API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "dashboard": "/dashboard"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/dashboard")
async def dashboard():
    """Dashboard endpoint"""
    # TODO: Return dashboard HTML
    return {"message": "Dashboard"}


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {settings.APP_NAME} on {settings.API_HOST}:{settings.API_PORT}")

    uvicorn.run(
        "src.backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
