"""
Generate Routes
Handles AI-powered suggestions and descriptions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class GenerateRequest(BaseModel):
    """Request model for AI generation"""
    product_info: Dict[str, Any]
    original_text: str
    language: str = "en"

class GenerateResponse(BaseModel):
    """Response model for AI generation"""
    success: bool
    description: str
    price_range: str
    where_to_sell: str
    selling_tip: str
    language: str
    error: Optional[str] = None

@router.post("/generate", response_model=GenerateResponse)
async def generate_ai_suggestions(request: GenerateRequest):
    """Generate AI-powered suggestions for product"""
    try:
        # This would integrate with the GeminiAIClient
        # For now, return mock response
        mock_suggestions = {
            'en': {
                "description": "Fresh, high-quality tomatoes from local farm. Perfect for daily cooking needs!",
                "price_range": "₹35 - ₹45 per kg",
                "where_to_sell": "Local market, nearby towns, or online agri-portals",
                "selling_tip": "Highlight freshness and organic quality to attract health-conscious buyers"
            },
            'hi': {
                "description": "स्थानीय खेत से ताजे, उच्च गुणवत्ता वाले टमाटर। दैनिक खाना पकाने के लिए बिल्कुल सही!",
                "price_range": "₹35 - ₹45 प्रति किलो",
                "where_to_sell": "स्थानीय बाजार, पास के शहर, या ऑनलाइन कृषि पोर्टल",
                "selling_tip": "स्वास्थ्य-जागरूक खरीदारों को आकर्षित करने के लिए ताजगी और जैविक गुणवत्ता पर जोर दें"
            },
            'ta': {
                "description": "உள்ளூர் பண்ணையில் இருந்து புதிய, உயர்தர தக்காளிகள். தினசரி சமையல் தேவைகளுக்கு சரியானது!",
                "price_range": "கிலோவுக்கு ₹35 - ₹45",
                "where_to_sell": "உள்ளூர் சந்தை, அருகிலுள்ள நகரங்கள், அல்லது ஆன்லைன் விவசாய போர்டல்கள்",
                "selling_tip": "ஆரோக்கியம் கவனிக்கும் வாங்குபவர்களை ஈர்க்க புதுமை மற்றும் கரிம தரத்தை முன்னிலைப்படுத்துங்கள்"
            }
        }
        
        suggestions = mock_suggestions.get(request.language, mock_suggestions['en'])
        
        return GenerateResponse(
            success=True,
            description=suggestions["description"],
            price_range=suggestions["price_range"],
            where_to_sell=suggestions["where_to_sell"],
            selling_tip=suggestions["selling_tip"],
            language=request.language
        )
        
    except Exception as e:
        logger.error(f"AI generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 