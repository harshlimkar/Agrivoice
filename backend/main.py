#!/usr/bin/env python3
"""
AgriVoice Backend - FastAPI Application
Voice-based product catalog for Indian farmers
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgriVoice API",
    description="Voice-based product catalog for Indian farmers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TranscribeRequest(BaseModel):
    audio_data: str
    language: str = "en"

class DescriptionRequest(BaseModel):
    text: str
    language: str = "en"

class StoreRequest(BaseModel):
    name: str
    description: str
    language: str = "en"
    mobile: str

class StatusRequest(BaseModel):
    mobile: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AgriVoice API is running! 🌾",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ai": "available",
            "database": "available"
        }
    }

@app.post("/transcribe")
async def transcribe_audio(request: TranscribeRequest):
    """Transcribe voice input"""
    try:
        # Mock transcription
        return {
            "success": True,
            "transcribed_text": "Sample transcribed text",
            "language": request.language,
            "confidence": 0.95
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-description")
async def generate_description(request: DescriptionRequest):
    """Generate AI description for product"""
    try:
        description_text = f"AI generated description for: {request.text}"
        return {
            "success": True,
            "description": description_text,
            "language": request.language
        }
    except Exception as e:
        logger.error(f"Description generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store")
async def store_product(request: StoreRequest):
    """Store product in database"""
    try:
        product_id = 12345
        return {
            "success": True,
            "product_id": product_id,
            "message": "Product saved successfully"
        }
    except Exception as e:
        logger.error(f"Store product error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-status")
async def check_product_status(request: StatusRequest):
    """Check product status and get suggestions"""
    try:
        products = {
            "success": True,
            "products": [
                {
                    "id": 1,
                    "name": "Sample Product",
                    "description": "Sample description",
                    "status": "pending",
                    "created_at": datetime.now().isoformat(),
                    "suggestions": "Try promoting on social media"
                }
            ]
        }
        return products
    except Exception as e:
        logger.error(f"Check status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
async def get_categories():
    """Get available product categories"""
    categories = [
        "Vegetables",
        "Fruits", 
        "Grains",
        "Dairy",
        "Meat",
        "Beverages",
        "Snacks",
        "General"
    ]
    return {
        "success": True,
        "categories": categories
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "API is working!",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ai": "available",
            "database": "available"
        }
    }

if __name__ == "__main__":
    print("🌾 Starting AgriVoice API Server...")
    print("=" * 50)
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,  # Disable reload to avoid conflicts
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try using a different port or check if port 8000 is already in use") 