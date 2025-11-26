"""
FastAPI Main Application for Portfolio Collaboration System.

Provides REST and WebSocket endpoints for web-based portfolio analysis.

Biblical Principle: SERVE - Simple, accessible API for powerful multi-agent analysis.
Biblical Principle: EXCELLENCE - Production-ready API with comprehensive error handling.

Usage:
    # Development server
    uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

    # Production server
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
"""

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.config import settings

# ============================================================================
# Logging Configuration
# ============================================================================

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format=settings.log_format,
    handlers=[
        logging.FileHandler(settings.logs_dir / "api.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ============================================================================
# Application Lifespan Management
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.

    Handles:
    - Startup: Verify environment, initialize resources
    - Shutdown: Cleanup resources, close connections
    """
    # Startup
    logger.info("=" * 80)
    logger.info("Portfolio Collaboration API Starting")
    logger.info("=" * 80)
    logger.info(f"Environment: {'Development' if settings.api_reload else 'Production'}")
    logger.info(f"Host: {settings.api_host}:{settings.api_port}")
    logger.info(f"CORS Origins: {', '.join(settings.cors_origins)}")
    logger.info(f"Project Root: {settings.project_root}")
    logger.info(f"Examples Dir: {settings.examples_dir}")
    logger.info(f"Outputs Dir: {settings.outputs_dir}")

    # Verify OpenAI API key
    if not settings.openai_api_key:
        logger.warning("⚠️  OPENAI_API_KEY not set - agent functionality will fail")
    else:
        logger.info("✓ OpenAI API key configured")

    # Verify examples directory exists
    if not settings.examples_dir.exists():
        logger.error(f"❌ Examples directory not found: {settings.examples_dir}")
    else:
        logger.info(f"✓ Examples directory found: {settings.examples_dir}")

    logger.info("=" * 80)
    logger.info("API Ready")
    logger.info("=" * 80)

    yield  # Application runs here

    # Shutdown
    logger.info("=" * 80)
    logger.info("Portfolio Collaboration API Shutting Down")
    logger.info("=" * 80)


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Portfolio Collaboration API",
    description=(
        "Multi-agent portfolio analysis system providing comprehensive risk, "
        "compliance, and performance analysis for financial advisors."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc",  # ReDoc
    openapi_url="/api/openapi.json",
)

# ============================================================================
# Middleware Configuration
# ============================================================================

# CORS Middleware - Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# ============================================================================
# Exception Handlers
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """
    Global exception handler for unhandled errors.

    Returns structured error response with logging.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "type": type(exc).__name__,
        },
    )


# ============================================================================
# Health Check Endpoints
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Portfolio Collaboration API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "openai_configured": bool(settings.openai_api_key),
    }


# ============================================================================
# Route Registration (Import routes after app is created)
# ============================================================================

# Import analysis and WebSocket routes
from src.api.routes import analysis, websocket

# Register routers
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(websocket.router, prefix="/api", tags=["WebSocket"])

logger.info("✓ Analysis and WebSocket API routes registered")

# ============================================================================
# Development Server Runner
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower(),
    )
