"""
Product schema Pydantic model
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProductStatus(str, Enum):
    """Product status enumeration"""
    PENDING = "pending"
    SOLD = "sold"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ProductCategory(str, Enum):
    """Product category enumeration"""
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    GRAINS = "grains"
    DAIRY = "dairy"
    MEAT = "meat"
    BEVERAGES = "beverages"
    SNACKS = "snacks"
    GENERAL = "general"

class ProductBase(BaseModel):
    """Base product model"""
    name: str = Field(..., min_length=2, max_length=200, description="Product name")
    description: str = Field(..., min_length=10, max_length=1000, description="Product description")
    language: str = Field(default="en", description="Language of description")
    farmer_mobile: str = Field(..., description="Farmer's mobile number")
    category: Optional[ProductCategory] = Field(None, description="Product category")
    price: Optional[float] = Field(None, ge=0, description="Product price in INR")
    quantity: Optional[str] = Field(None, max_length=50, description="Product quantity")
    unit: Optional[str] = Field(None, max_length=20, description="Unit of measurement")

class ProductCreate(ProductBase):
    """Model for creating a new product"""
    pass

class ProductUpdate(BaseModel):
    """Model for updating product information"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    category: Optional[ProductCategory] = Field(None)
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[str] = Field(None, max_length=50)
    unit: Optional[str] = Field(None, max_length=20)
    status: Optional[ProductStatus] = Field(None)

class ProductResponse(ProductBase):
    """Model for product response"""
    id: str = Field(..., description="Product ID")
    status: ProductStatus = Field(default=ProductStatus.PENDING, description="Product status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    suggestions: Optional[str] = Field(None, description="AI-generated suggestions")
    
    class Config:
        from_attributes = True

class ProductStatusUpdate(BaseModel):
    """Model for updating product status"""
    status: ProductStatus = Field(..., description="New product status")
    
    @validator('status')
    def validate_status_transition(cls, v):
        """Validate status transition"""
        valid_transitions = {
            ProductStatus.PENDING: [ProductStatus.SOLD, ProductStatus.CANCELLED, ProductStatus.EXPIRED],
            ProductStatus.SOLD: [ProductStatus.PENDING],  # Allow reverting for demo
            ProductStatus.CANCELLED: [ProductStatus.PENDING],
            ProductStatus.EXPIRED: [ProductStatus.PENDING]
        }
        return v

class ProductSearch(BaseModel):
    """Model for product search"""
    query: str = Field(..., min_length=1, max_length=100, description="Search query")
    language: Optional[str] = Field(None, description="Language filter")
    category: Optional[ProductCategory] = Field(None, description="Category filter")
    status: Optional[ProductStatus] = Field(None, description="Status filter")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    
    @validator('max_price')
    def validate_price_range(cls, v, values):
        """Validate price range"""
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('Maximum price must be greater than minimum price')
        return v

class ProductStats(BaseModel):
    """Model for product statistics"""
    total_products: int = Field(..., ge=0, description="Total number of products")
    sold_products: int = Field(..., ge=0, description="Number of sold products")
    pending_products: int = Field(..., ge=0, description="Number of pending products")
    expired_products: int = Field(..., ge=0, description="Number of expired products")
    cancelled_products: int = Field(..., ge=0, description="Number of cancelled products")
    sold_percentage: float = Field(..., ge=0, le=100, description="Percentage of sold products")
    average_price: Optional[float] = Field(None, ge=0, description="Average product price")
    total_value: Optional[float] = Field(None, ge=0, description="Total value of products")

    @validator('sold_percentage')
    def validate_sold_percentage(cls, v, values):
        """Validate sold percentage"""
        if 'total_products' in values and values['total_products'] > 0:
            calculated = (values['sold_products'] / values['total_products']) * 100
            if abs(v - calculated) > 0.1:  # Allow small rounding differences
                raise ValueError('Sold percentage does not match calculated value')
        return v

class ProductAnalytics(BaseModel):
    """Model for product analytics"""
    daily_uploads: List[dict] = Field(default_factory=list, description="Daily upload statistics")
    category_distribution: List[dict] = Field(default_factory=list, description="Category distribution")
    price_distribution: List[dict] = Field(default_factory=list, description="Price distribution")
    language_distribution: List[dict] = Field(default_factory=list, description="Language distribution")
    status_timeline: List[dict] = Field(default_factory=list, description="Status change timeline")

class ProductSuggestion(BaseModel):
    """Model for product suggestions"""
    product_id: str = Field(..., description="Product ID")
    suggestions: str = Field(..., description="AI-generated suggestions")
    language: str = Field(..., description="Language of suggestions")
    created_at: datetime = Field(..., description="Suggestion timestamp")

class VoiceInput(BaseModel):
    """Model for voice input processing"""
    audio: str = Field(..., description="Base64 encoded audio data")
    language: str = Field(..., description="Language code")
    
    @validator('language')
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = [
            'en', 'hi', 'ta', 'te', 'kn', 'ml', 'gu', 'mr', 'bn', 'or', 'pa'
        ]
        if v not in valid_languages:
            raise ValueError(f'Invalid language code. Must be one of: {valid_languages}')
        return v

class TranscriptionResult(BaseModel):
    """Model for transcription result"""
    success: bool = Field(..., description="Transcription success status")
    text: Optional[str] = Field(None, description="Transcribed text")
    language: str = Field(..., description="Language used")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")
    error: Optional[str] = Field(None, description="Error message if failed")

class DescriptionGeneration(BaseModel):
    """Model for description generation"""
    text: str = Field(..., description="Transcribed text")
    language: str = Field(..., description="Language code")
    
    @validator('text')
    def validate_text(cls, v):
        """Validate transcribed text"""
        if not v.strip():
            raise ValueError('Transcribed text cannot be empty')
        return v.strip()

class GeneratedDescription(BaseModel):
    """Model for generated description result"""
    success: bool = Field(..., description="Generation success status")
    description: Optional[str] = Field(None, description="Generated description")
    language: str = Field(..., description="Language used")
    original_text: str = Field(..., description="Original transcribed text")
    error: Optional[str] = Field(None, description="Error message if failed") 