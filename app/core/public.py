from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint - public access"""
    return {
        "status": "healthy",
        "message": "Embrapa Vitiviniculture API is running",
        "authentication": "JWT enabled",
    }


@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Embrapa Vitiviniculture API",
        "version": "1.0.0",
        "description": "API for Brazilian wine industry data",
        "authentication": "JWT Bearer Token required for protected endpoints",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
