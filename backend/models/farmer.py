"""
Pydantic model for farmer
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class FarmerBase(BaseModel):
    """Base farmer model"""
    name: str = Field(..., min_length=2, max_length=100, description="Farmer's full name")
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")
    language: str = Field(default="en", description="Preferred language")
    village_city: str = Field(..., min_length=2, max_length=100, description="Village or city name")

class FarmerCreate(FarmerBase):
    """Model for creating a new farmer"""
    pass

class FarmerUpdate(BaseModel):
    """Model for updating farmer information"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    language: Optional[str] = Field(None)
    village_city: Optional[str] = Field(None, min_length=2, max_length=100)

class FarmerResponse(FarmerBase):
    """Model for farmer response"""
    id: str = Field(..., description="Farmer ID")
    created_at: datetime = Field(..., description="Registration timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True

class FarmerLogin(BaseModel):
    """Model for farmer login"""
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")
    otp: Optional[str] = Field(None, pattern=r'^\d{6}$', description="6-digit OTP")

class OTPRequest(BaseModel):
    """Model for OTP request"""
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")

class OTPVerify(BaseModel):
    """Model for OTP verification"""
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")
    otp: str = Field(..., pattern=r'^\d{6}$', description="6-digit OTP")

class FarmerStats(BaseModel):
    """Model for farmer statistics"""
    total_products: int = Field(..., ge=0, description="Total number of products")
    sold_products: int = Field(..., ge=0, description="Number of sold products")
    pending_products: int = Field(..., ge=0, description="Number of pending products")
    sold_percentage: float = Field(..., ge=0, le=100, description="Percentage of sold products")
    registration_date: datetime = Field(..., description="Registration date")
    last_activity: datetime = Field(..., description="Last activity date")

    @validator('sold_percentage')
    def validate_sold_percentage(cls, v, values):
        """Validate sold percentage"""
        if 'total_products' in values and values['total_products'] > 0:
            calculated = (values['sold_products'] / values['total_products']) * 100
            if abs(v - calculated) > 0.1:  # Allow small rounding differences
                raise ValueError('Sold percentage does not match calculated value')
        return v

class FarmerProfile(BaseModel):
    """Model for farmer profile"""
    id: str = Field(..., description="Farmer ID")
    name: str = Field(..., description="Farmer's name")
    mobile: str = Field(..., description="Mobile number")
    language: str = Field(..., description="Preferred language")
    village_city: str = Field(..., description="Village or city")
    stats: FarmerStats = Field(..., description="Farmer statistics")
    created_at: datetime = Field(..., description="Registration date")
    updated_at: datetime = Field(..., description="Last update date")

    class Config:
        from_attributes = True

class LanguagePreference(BaseModel):
    """Model for language preference"""
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

class MobileValidation(BaseModel):
    """Model for mobile number validation"""
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit mobile number")
    
    @validator('mobile')
    def validate_mobile(cls, v):
        """Validate mobile number format"""
        if not v.isdigit():
            raise ValueError('Mobile number must contain only digits')
        if len(v) != 10:
            raise ValueError('Mobile number must be exactly 10 digits')
        if not v.startswith(('6', '7', '8', '9')):
            raise ValueError('Mobile number must start with 6, 7, 8, or 9')
        return v 