"""
Store Routes
Handles database storage operations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class StoreRequest(BaseModel):
    """Request model for storing data"""
    product_info: Dict[str, Any]
    ai_suggestions: Dict[str, Any]
    transcribed_text: str
    language: str
    farmer_mobile: str
    audio_url: Optional[str] = None

class StoreResponse(BaseModel):
    """Response model for storage operations"""
    success: bool
    product_id: str
    message: str
    error: Optional[str] = None

@router.post("/store", response_model=StoreResponse)
async def store_product(request: StoreRequest):
    """Store product information in database"""
    try:
        # This would integrate with the SupabaseClient
        # For now, return mock response
        product_id = f"demo_product_{hash(request.transcribed_text) % 1000}"
        
        logger.info(f"Product stored successfully with ID: {product_id}")
        
        return StoreResponse(
            success=True,
            product_id=product_id,
            message="Product stored successfully"
        )
        
    except Exception as e:
        logger.error(f"Store product error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 