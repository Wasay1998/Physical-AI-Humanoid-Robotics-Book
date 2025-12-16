from fastapi import APIRouter
from typing import Dict
from datetime import datetime


router = APIRouter()


@router.get("/health", summary="Health check endpoint")
async def get_health() -> Dict:
    """
    Check the health status of the API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }