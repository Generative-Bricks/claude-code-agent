"""
API Routes for Portfolio Collaboration System.

Exports all route modules for easy import in main application.

Biblical Principle: EXCELLENCE - Well-organized, modular routing structure.
"""

from src.api.routes import analysis, websocket

__all__ = ["analysis", "websocket"]
