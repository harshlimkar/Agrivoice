"""
Status Routes
Handles health checks and system status
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class StatusResponse(BaseModel):
    """Response model for status checks"""
    status: str
    message: str
    version: str
    services: Dict[str, Any]

@router.get("/status", response_model=StatusResponse)
async def get_system_status():
    """Get system status and health check"""
    try:
        # Mock service status for demo
        services = {
            "ai": {
                "status": "available",
                "model": "gemini-pro",
                "api_key_configured": True
            },
            "database": {
                "status": "connected",
                "type": "supabase",
                "url_configured": True
            },
            "audio": {
                "status": "available",
                "formats": ["wav", "mp3", "ogg"],
                "languages": ["en", "hi", "ta", "te", "kn", "ml", "gu", "mr", "bn", "or", "pa"]
            }
        }
        
        return StatusResponse(
            status="healthy",
            message="AgriVoice API is running",
            version="1.0.0",
            services=services
        )
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return StatusResponse(
            status="degraded",
            message="System experiencing issues",
            version="1.0.0",
            services={}
        ) 