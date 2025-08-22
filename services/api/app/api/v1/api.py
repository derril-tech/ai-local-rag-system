"""
Main API router for AI Local RAG System
"""
from fastapi import APIRouter

# Import and include all API endpoint routers
from .auth import router as auth_router
from .collections import router as collections_router
from .documents import router as documents_router
from .chat import router as chat_router
from .connectors import router as connectors_router
from .admin import router as admin_router

api_router = APIRouter()

# Include all API routers
api_router.include_router(auth_router)
api_router.include_router(collections_router)
api_router.include_router(documents_router)
api_router.include_router(chat_router)
api_router.include_router(connectors_router)
api_router.include_router(admin_router)

# Placeholder endpoint for development
@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "AI Local RAG System API",
        "version": "1.0.0",
        "status": "development"
    }
