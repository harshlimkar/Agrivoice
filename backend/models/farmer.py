"""
Farmer models for AgriVoice
Pydantic schemas for farmer data validation
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class FarmerCreate(BaseModel):
    """Schema for creating a new farmer account"""
    name: str = Field(..., min_length=2, max_length=100, description="Farmer's full name")
    email: EmailStr = Field(..., description="Farmer's email address")
    phone: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")
    password: str = Field(..., min_length=6, description="Password")
    language: str = Field(default="en", description="Preferred language")
    village_city: Optional[str] = Field(None, max_length=100, description="Village or city")

class FarmerResponse(BaseModel):
    """Schema for farmer response"""
    id: str
    name: str
    email: str
    phone: str
    language: str
    village_city: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

class FarmerLogin(BaseModel):
    """Schema for farmer login"""
    email: EmailStr = Field(..., description="Farmer's email address")
    password: str = Field(..., description="Password")

class FarmerUpdate(BaseModel):
    """Schema for updating farmer information"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, pattern=r'^[6-9]\d{9}$')
    language: Optional[str] = Field(None)
    village_city: Optional[str] = Field(None, max_length=100)

class FarmerStats(BaseModel):
    """Schema for farmer statistics"""
    total_products: int = Field(..., ge=0, description="Total products uploaded")
    sold_products: int = Field(..., ge=0, description="Number of sold products")
    pending_products: int = Field(..., ge=0, description="Number of pending products")
    total_revenue: float = Field(..., ge=0, description="Total revenue from sold products")
    success_rate: float = Field(..., ge=0, le=100, description="Success rate percentage") 