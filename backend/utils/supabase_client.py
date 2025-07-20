"""
Supabase Client for AgriVoice
Handles database operations for products and farmers
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Client for interacting with Supabase database"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase credentials not found in environment variables")
            self.client = None
        else:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.client = None
    
    async def store_product(self, product_info: Dict[str, Any], 
                          ai_suggestions: Dict[str, Any],
                          transcribed_text: str,
                          language: str,
                          farmer_mobile: str,
                          audio_url: Optional[str] = None) -> Dict[str, Any]:
        """Store product information in database"""
        try:
            if not self.client:
                return self._mock_store_product(product_info, ai_suggestions, transcribed_text, language, farmer_mobile)
            
            data = {
                "farmer_mobile": farmer_mobile,
                "product_info": json.dumps(product_info),
                "ai_suggestions": json.dumps(ai_suggestions),
                "transcribed_text": transcribed_text,
                "language": language,
                "audio_url": audio_url,
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            
            result = self.client.table("products").insert(data).execute()
            
            if result.data:
                logger.info(f"Product stored successfully with ID: {result.data[0]['id']}")
                return result.data[0]
            else:
                raise Exception("Failed to store product")
                
        except Exception as e:
            logger.error(f"Error storing product: {e}")
            return self._mock_store_product(product_info, ai_suggestions, transcribed_text, language, farmer_mobile)
    
    async def get_products_by_mobile(self, mobile: str) -> List[Dict[str, Any]]:
        """Get products by farmer mobile number"""
        try:
            if not self.client:
                return self._mock_get_products(mobile)
            
            result = self.client.table("products").select("*").eq("farmer_mobile", mobile).execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} products for mobile: {mobile}")
                return result.data
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return self._mock_get_products(mobile)
    
    async def update_product_status(self, product_id: str, status: str) -> Dict[str, Any]:
        """Update product status"""
        try:
            if not self.client:
                return {"success": True, "message": "Status updated (demo mode)"}
            
            data = {
                "status": status,
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.client.table("products").update(data).eq("id", product_id).execute()
            
            if result.data:
                logger.info(f"Product {product_id} status updated to: {status}")
                return {"success": True, "message": "Status updated successfully"}
            else:
                raise Exception("Failed to update product status")
                
        except Exception as e:
            logger.error(f"Error updating product status: {e}")
            return {"success": False, "message": str(e)}
    
    async def get_unsold_products(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get unsold products older than specified days"""
        try:
            if not self.client:
                return self._mock_get_unsold_products(days)
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            result = self.client.table("products").select("*").eq("status", "pending").lt("created_at", cutoff_date).execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} unsold products older than {days} days")
                return result.data
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting unsold products: {e}")
            return self._mock_get_unsold_products(days)
    
    async def update_product_suggestions(self, product_id: str, suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """Update product with improvement suggestions"""
        try:
            if not self.client:
                return {"success": True, "message": "Suggestions updated (demo mode)"}
            
            data = {
                "improvement_suggestions": json.dumps(suggestions),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.client.table("products").update(data).eq("id", product_id).execute()
            
            if result.data:
                logger.info(f"Product {product_id} suggestions updated")
                return {"success": True, "message": "Suggestions updated successfully"}
            else:
                raise Exception("Failed to update product suggestions")
                
        except Exception as e:
            logger.error(f"Error updating product suggestions: {e}")
            return {"success": False, "message": str(e)}
    
    async def register_farmer(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new farmer"""
        try:
            if not self.client:
                return self._mock_register_farmer(farmer_data)
            
            data = {
                "name": farmer_data["name"],
                "email": farmer_data["email"],
                "phone": farmer_data["phone"],
                "language": farmer_data.get("language", "en"),
                "village_city": farmer_data.get("village_city"),
                "created_at": datetime.now().isoformat()
            }
            
            result = self.client.table("farmers").insert(data).execute()
            
            if result.data:
                logger.info(f"Farmer registered successfully: {result.data[0]['id']}")
                return result.data[0]
            else:
                raise Exception("Failed to register farmer")
                
        except Exception as e:
            logger.error(f"Error registering farmer: {e}")
            return self._mock_register_farmer(farmer_data)
    
    async def login_farmer(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Login farmer"""
        try:
            if not self.client:
                return self._mock_login_farmer(credentials)
            
            result = self.client.table("farmers").select("*").eq("email", credentials["email"]).execute()
            
            if result.data:
                farmer = result.data[0]
                # In production, you would verify password hash here
                logger.info(f"Farmer logged in: {farmer['id']}")
                return farmer
            else:
                raise Exception("Invalid credentials")
                
        except Exception as e:
            logger.error(f"Error logging in farmer: {e}")
            return self._mock_login_farmer(credentials)
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get database connection status"""
        return {
            "connected": self.client is not None,
            "url_configured": self.supabase_url is not None,
            "key_configured": self.supabase_key is not None
        }
    
    # Mock methods for demo purposes
    def _mock_store_product(self, product_info: Dict[str, Any], 
                           ai_suggestions: Dict[str, Any],
                           transcribed_text: str,
                           language: str,
                           farmer_mobile: str) -> Dict[str, Any]:
        """Mock product storage for demo"""
        return {
            "id": "demo_product_123",
            "farmer_mobile": farmer_mobile,
            "product_info": json.dumps(product_info),
            "ai_suggestions": json.dumps(ai_suggestions),
            "transcribed_text": transcribed_text,
            "language": language,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
    
    def _mock_get_products(self, mobile: str) -> List[Dict[str, Any]]:
        """Mock product retrieval for demo"""
        return [
            {
                "id": "demo_product_123",
                "farmer_mobile": mobile,
                "product_info": '{"product": "tomato", "quantity": "10 kg", "price": "₹40"}',
                "ai_suggestions": '{"description": "Fresh tomatoes", "price_range": "₹35-45"}',
                "transcribed_text": "I have 10 kg of tomatoes",
                "language": "en",
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def _mock_get_unsold_products(self, days: int) -> List[Dict[str, Any]]:
        """Mock unsold products for demo"""
        return [
            {
                "id": "demo_unsold_123",
                "product_info": '{"product": "onion", "quantity": "5 kg", "price": "₹30"}',
                "language": "en",
                "created_at": (datetime.now() - timedelta(days=days + 1)).isoformat()
            }
        ]
    
    def _mock_register_farmer(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock farmer registration for demo"""
        return {
            "id": "demo_farmer_123",
            "name": farmer_data["name"],
            "email": farmer_data["email"],
            "phone": farmer_data["phone"],
            "language": farmer_data.get("language", "en"),
            "village_city": farmer_data.get("village_city"),
            "created_at": datetime.now().isoformat()
        }
    
    def _mock_login_farmer(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Mock farmer login for demo"""
        return {
            "id": "demo_farmer_123",
            "name": "Demo Farmer",
            "email": credentials["email"],
            "phone": "9876543210",
            "language": "en",
            "village_city": "Demo Village",
            "created_at": datetime.now().isoformat()
        } 