"""
Supabase store route for database operations
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime
from utils.supabase_client import SupabaseClient

async def save_product(name: str, description: str, language: str, mobile: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Save product to Supabase database
    
    Args:
        name: Product name
        description: Product description
        language: Language code
        mobile: Farmer's mobile number
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing save result
    """
    try:
        # Create product data
        product_data = {
            "name": name,
            "description": description,
            "language": language,
            "farmer_mobile": mobile,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Save to database
        result = await supabase_client.insert_product(product_data)
        
        return {
            "success": True,
            "product_id": result.get("id"),
            "message": "Product saved successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to save product: {str(e)}"
        }

async def get_products_by_mobile(mobile: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Get products by farmer's mobile number
    
    Args:
        mobile: Farmer's mobile number
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing products list
    """
    try:
        # Get products from database
        products = await supabase_client.get_products_by_mobile(mobile)
        
        return {
            "success": True,
            "products": products,
            "count": len(products)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get products: {str(e)}",
            "products": get_mock_products(mobile)  # Fallback to mock data
        }

async def update_product_status(product_id: str, status: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Update product status (sold/pending)
    
    Args:
        product_id: Product ID
        status: New status (sold/pending)
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing update result
    """
    try:
        # Update product status
        result = await supabase_client.update_product_status(product_id, status)
        
        return {
            "success": True,
            "product_id": product_id,
            "status": status,
            "message": f"Product status updated to {status}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update product status: {str(e)}"
        }

async def save_farmer(farmer_data: Dict[str, Any], supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Save farmer registration data
    
    Args:
        farmer_data: Farmer information
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing save result
    """
    try:
        # Add timestamps
        farmer_data.update({
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        # Save to database
        result = await supabase_client.insert_farmer(farmer_data)
        
        return {
            "success": True,
            "farmer_id": result.get("id"),
            "message": "Farmer registered successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to register farmer: {str(e)}"
        }

async def get_farmer_by_mobile(mobile: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Get farmer by mobile number
    
    Args:
        mobile: Farmer's mobile number
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing farmer data
    """
    try:
        # Get farmer from database
        farmer = await supabase_client.get_farmer_by_mobile(mobile)
        
        return {
            "success": True,
            "farmer": farmer
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get farmer: {str(e)}"
        }

def get_mock_products(mobile: str) -> List[Dict[str, Any]]:
    """
    Get mock products for demo purposes
    
    Args:
        mobile: Farmer's mobile number
        
    Returns:
        List of mock products
    """
    return [
        {
            "id": "1",
            "name": "Fresh Tomatoes",
            "description": "Fresh, high-quality tomatoes from local farm. Perfect for your daily needs!",
            "language": "en",
            "farmer_mobile": mobile,
            "status": "pending",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "suggestions": "Try adding better photos and highlighting freshness"
        },
        {
            "id": "2",
            "name": "Organic Rice",
            "description": "Premium quality organic rice, perfect for daily meals",
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
            "updated_at": "2024-01-13T09:20:00Z",
            "suggestions": "Consider competitive pricing and quick delivery"
        }
    ]

def get_mock_farmer(mobile: str) -> Dict[str, Any]:
    """
    Get mock farmer data for demo purposes
    
    Args:
        mobile: Farmer's mobile number
        
    Returns:
        Mock farmer data
    """
    return {
        "id": "1",
        "name": "Rajesh Kumar",
        "mobile": mobile,
        "language": "en",
        "village_city": "Mumbai",
        "created_at": "2024-01-10T08:00:00Z",
        "updated_at": "2024-01-10T08:00:00Z"
    }

async def delete_product(product_id: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Delete product from database
    
    Args:
        product_id: Product ID
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing delete result
    """
    try:
        # Delete product from database
        result = await supabase_client.delete_product(product_id)
        
        return {
            "success": True,
            "product_id": product_id,
            "message": "Product deleted successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete product: {str(e)}"
        }

async def search_products(query: str, language: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Search products by query
    
    Args:
        query: Search query
        language: Language code
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing search results
    """
    try:
        # Search products in database
        products = await supabase_client.search_products(query, language)
        
        return {
            "success": True,
            "products": products,
            "count": len(products),
            "query": query
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to search products: {str(e)}",
            "products": []
        }

async def get_product_statistics(mobile: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Get product statistics for farmer
    
    Args:
        mobile: Farmer's mobile number
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing statistics
    """
    try:
        # Get products for statistics
        products = await supabase_client.get_products_by_mobile(mobile)
        
        # Calculate statistics
        total_products = len(products)
        sold_products = len([p for p in products if p.get("status") == "sold"])
        pending_products = total_products - sold_products
        
        return {
            "success": True,
            "statistics": {
                "total": total_products,
                "sold": sold_products,
                "pending": pending_products,
                "sold_percentage": (sold_products / total_products * 100) if total_products > 0 else 0
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get statistics: {str(e)}",
            "statistics": {
                "total": 0,
                "sold": 0,
                "pending": 0,
                "sold_percentage": 0
            }
        } 