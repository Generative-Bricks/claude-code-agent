"""
API module for Portfolio Collaboration System.

Provides FastAPI-based REST and WebSocket endpoints for web interface integration.

Biblical Principle: SERVE - Making multi-agent analysis accessible via modern web APIs.
Biblical Principle: TRUTH - All analysis results are transparent and traceable.
"""

# Lazy import to avoid FastAPI dependency when only using schemas
try:
    from src.api.main import app
    __all__ = ["app"]
except ImportError:
    # FastAPI not installed - schemas can still be used
    __all__ = []
