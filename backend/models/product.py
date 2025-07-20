"""
Product models for AgriVoice
Pydantic schemas for product data validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ProductCreate(BaseModel):
    """Schema for creating a new product"""
    product: str = Field(..., description="Product name")
    quantity: str = Field(..., description="Quantity with unit")
    price: str = Field(..., description="Price with currency")
    description: Optional[str] = Field(None, description="Product description")
    language: str = Field(default="en", description="Language code")
    farmer_mobile: str = Field(..., description="Farmer's mobile number")

class ProductResponse(BaseModel):
    """Schema for product response"""
    id: str
    product: str
    quantity: str
    price: str
    description: Optional[str]
    language: str
    farmer_mobile: str
    status: str = Field(default="pending", description="Product status")
    created_at: datetime
    updated_at: Optional[datetime] = None

class VoiceProcessRequest(BaseModel):
    """Schema for voice processing request"""
    audio_data: Optional[str] = Field(None, description="Base64 encoded audio data")
    transcribed_text: Optional[str] = Field(None, description="Pre-transcribed text")
    language: str = Field(default="en", description="Language code")
    farmer_mobile: Optional[str] = Field(None, description="Farmer's mobile number")

class ProductInfo(BaseModel):
    """Schema for extracted product information"""
    product: str
    quantity: str
    price: str
    price_per_unit: Optional[str] = None

class AIResponse(BaseModel):
    """Schema for AI-generated response"""
    description: str
    price_range: str
    where_to_sell: str
    selling_tip: str

class StoreProductRequest(BaseModel):
    """Schema for storing product in database"""
    product_info: Dict[str, Any]
    ai_response: Dict[str, Any]
    transcribed_text: str
    language: str
    farmer_mobile: str
    audio_url: Optional[str] = None

class ProductStatusUpdate(BaseModel):
    """Schema for updating product status"""
    product_id: str
    status: str = Field(..., pattern="^(sold|pending|expired)$")

class ProductSearchRequest(BaseModel):
    """Schema for searching products"""
    farmer_mobile: str
    status: Optional[str] = None
    language: Optional[str] = None 