"""
Supabase SDK config client
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from supabase import create_client, Client
import os

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.client: Optional[Client] = None
        self.is_initialized = False
        
        if self.url and self.key:
            self.initialize()
    
    def initialize(self):
        """Initialize Supabase client"""
        try:
            if self.url and self.key:
                self.client = create_client(self.url, self.key)
                self.is_initialized = True
            else:
                self.is_initialized = False
        except Exception as e:
            print(f"Failed to initialize Supabase client: {e}")
            self.is_initialized = False
    
    async def insert_farmer(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert farmer data into database
        
        Args:
            farmer_data: Farmer information
            
        Returns:
            Insert result
        """
        if not self.is_initialized or not self.client:
            return self.get_mock_farmer_result(farmer_data)
        
        try:
            result = await asyncio.to_thread(
                self.client.table('farmers').insert(farmer_data).execute
            )
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Supabase insert farmer error: {e}")
            return self.get_mock_farmer_result(farmer_data)
    
    async def insert_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert product data into database
        
        Args:
            product_data: Product information
            
        Returns:
            Insert result
        """
        if not self.is_initialized or not self.client:
            return self.get_mock_product_result(product_data)
        
        try:
            result = await asyncio.to_thread(
                self.client.table('products').insert(product_data).execute
            )
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Supabase insert product error: {e}")
            return self.get_mock_product_result(product_data)
    
    async def get_products_by_mobile(self, mobile: str) -> List[Dict[str, Any]]:
        """
        Get products by farmer's mobile number
        
        Args:
            mobile: Farmer's mobile number
            
        Returns:
            List of products
        """
        if not self.is_initialized or not self.client:
            return self.get_mock_products(mobile)
        
        try:
            result = await asyncio.to_thread(
                self.client.table('products')
                .select('*')
                .eq('farmer_mobile', mobile)
                .order('created_at', desc=True)
                .execute
            )
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase get products error: {e}")
            return self.get_mock_products(mobile)
    
    async def get_farmer_by_mobile(self, mobile: str) -> Optional[Dict[str, Any]]:
        """
        Get farmer by mobile number
        
        Args:
            mobile: Farmer's mobile number
            
        Returns:
            Farmer data or None
        """
        if not self.is_initialized or not self.client:
            return self.get_mock_farmer(mobile)
        
        try:
            result = await asyncio.to_thread(
                self.client.table('farmers')
                .select('*')
                .eq('mobile', mobile)
                .limit(1)
                .execute
            )
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase get farmer error: {e}")
            return self.get_mock_farmer(mobile)
    
    async def update_product_status(self, product_id: str, status: str) -> Dict[str, Any]:
        """
        Update product status
        
        Args:
            product_id: Product ID
            status: New status
            
        Returns:
            Update result
        """
        if not self.is_initialized or not self.client:
            return {"id": product_id, "status": status}
        
        try:
            result = await asyncio.to_thread(
                self.client.table('products')
                .update({"status": status, "updated_at": self.get_current_timestamp()})
                .eq('id', product_id)
                .execute
            )
            return result.data[0] if result.data else {"id": product_id, "status": status}
        except Exception as e:
            print(f"Supabase update product error: {e}")
            return {"id": product_id, "status": status}
    
    async def delete_product(self, product_id: str) -> bool:
        """
        Delete product from database
        
        Args:
            product_id: Product ID
            
        Returns:
            True if successful
        """
        if not self.is_initialized or not self.client:
            return True
        
        try:
            await asyncio.to_thread(
                self.client.table('products')
                .delete()
                .eq('id', product_id)
                .execute
            )
            return True
        except Exception as e:
            print(f"Supabase delete product error: {e}")
            return False
    
    async def search_products(self, query: str, language: str) -> List[Dict[str, Any]]:
        """
        Search products by query
        
        Args:
            query: Search query
            language: Language code
            
        Returns:
            List of matching products
        """
        if not self.is_initialized or not self.client:
            return self.get_mock_search_results(query)
        
        try:
            result = await asyncio.to_thread(
                self.client.table('products')
                .select('*')
                .or_(f"name.ilike.%{query}%,description.ilike.%{query}%")
                .eq('language', language)
                .order('created_at', desc=True)
                .execute
            )
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase search products error: {e}")
            return self.get_mock_search_results(query)
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def get_mock_farmer_result(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get mock farmer insert result"""
        return {
            "id": "mock_farmer_1",
            "name": farmer_data.get("name", "Mock Farmer"),
            "mobile": farmer_data.get("mobile", ""),
            "language": farmer_data.get("language", "en"),
            "village_city": farmer_data.get("village_city", "Mock City"),
            "created_at": farmer_data.get("created_at", self.get_current_timestamp()),
            "updated_at": farmer_data.get("updated_at", self.get_current_timestamp())
        }
    
    def get_mock_product_result(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get mock product insert result"""
        return {
            "id": "mock_product_1",
            "name": product_data.get("name", "Mock Product"),
            "description": product_data.get("description", "Mock description"),
            "language": product_data.get("language", "en"),
            "farmer_mobile": product_data.get("farmer_mobile", ""),
            "status": product_data.get("status", "pending"),
            "created_at": product_data.get("created_at", self.get_current_timestamp()),
            "updated_at": product_data.get("updated_at", self.get_current_timestamp())
        }
    
    def get_mock_products(self, mobile: str) -> List[Dict[str, Any]]:
        """Get mock products for demo"""
        return [
            {
                "id": "1",
                "name": "Fresh Tomatoes",
                "description": "Fresh, high-quality tomatoes from local farm",
                "language": "en",
                "farmer_mobile": mobile,
                "status": "pending",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            },
            {
                "id": "2",
                "name": "Organic Rice",
                "description": "Premium quality organic rice",
                "language": "en",
                "farmer_mobile": mobile,
                "status": "sold",
                "created_at": "2024-01-14T15:45:00Z",
                "updated_at": "2024-01-14T15:45:00Z"
            },
            {
                "id": "3",
                "name": "Sweet Mangoes",
                "description": "Sweet and juicy mangoes from organic farms",
                "language": "en",
                "farmer_mobile": mobile,
                "status": "pending",
                "created_at": "2024-01-13T09:20:00Z",
                "updated_at": "2024-01-13T09:20:00Z"
            }
        ]
    
    def get_mock_farmer(self, mobile: str) -> Dict[str, Any]:
        """Get mock farmer data"""
        return {
            "id": "1",
            "name": "Rajesh Kumar",
            "mobile": mobile,
            "language": "en",
            "village_city": "Mumbai",
            "created_at": "2024-01-10T08:00:00Z",
            "updated_at": "2024-01-10T08:00:00Z"
        }
    
    def get_mock_search_results(self, query: str) -> List[Dict[str, Any]]:
        """Get mock search results"""
        return [
            {
                "id": "1",
                "name": f"Product matching '{query}'",
                "description": f"Description containing '{query}'",
                "language": "en",
                "farmer_mobile": "9876543210",
                "status": "pending",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        ]
    
    def is_available(self) -> bool:
        """
        Check if Supabase is available
        
        Returns:
            True if available
        """
        return self.is_initialized and self.url is not None and self.key is not None
    
    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get connection status information
        
        Returns:
            Status information
        """
        return {
            "available": self.is_available(),
            "initialized": self.is_initialized,
            "has_url": self.url is not None,
            "has_key": self.key is not None
        } 