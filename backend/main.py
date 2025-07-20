"""
AgriVoice - Main FastAPI Application
Orchestrates the complete voice-to-product workflow
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Import our modules
from models.farmer import FarmerCreate, FarmerResponse
from models.product import ProductCreate, ProductResponse, VoiceProcessRequest
from routes import transcribe, generate, store, status
from utils.ai_client import GeminiAIClient
from utils.audio_tools import AudioProcessor
from utils.supabase_client import SupabaseClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgriVoice API",
    description="Multilingual AI-powered voice product catalog for Indian farmers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get frontend path
frontend_path = Path(__file__).resolve().parent.parent / "frontend"

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Initialize clients
ai_client = GeminiAIClient()
audio_processor = AudioProcessor()
supabase_client = SupabaseClient()

# Include routers
app.include_router(transcribe.router, prefix="/api", tags=["transcribe"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(store.router, prefix="/api", tags=["store"])
app.include_router(status.router, prefix="/api", tags=["status"])

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main index.html page"""
    try:
        with open(frontend_path / "index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend files not found</h1>", status_code=404)

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    """Serve the login page"""
    try:
        with open(frontend_path / "login.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Login page not found</h1>", status_code=404)

@app.get("/register", response_class=HTMLResponse)
async def get_register():
    """Serve the register page"""
    try:
        with open(frontend_path / "register.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Register page not found</h1>", status_code=404)

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the dashboard page"""
    try:
        with open(frontend_path / "dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard page not found</h1>", status_code=404)

@app.get("/upload", response_class=HTMLResponse)
async def get_upload():
    """Serve the upload page"""
    try:
        with open(frontend_path / "upload.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Upload page not found</h1>", status_code=404)

@app.get("/status", response_class=HTMLResponse)
async def get_status():
    """Serve the status page"""
    try:
        with open(frontend_path / "status.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Status page not found</h1>", status_code=404)

# API Routes
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="AgriVoice API is running",
        version="1.0.0"
    )

@app.post("/api/complete-voice-process")
async def complete_voice_process(request: VoiceProcessRequest):
    """
    Complete voice processing workflow:
    1. Speech-to-Text conversion
    2. Product information extraction
    3. AI-powered suggestions generation
    4. Data storage in Supabase
    """
    try:
        logger.info(f"Processing voice input in language: {request.language}")
        
        # Step 1: Speech-to-Text conversion
        if request.audio_data:
            transcribed_text = await audio_processor.process_audio(request.audio_data, request.language)
        elif request.transcribed_text:
            transcribed_text = request.transcribed_text
        else:
            raise HTTPException(status_code=400, detail="Either audio_data or transcribed_text must be provided")
        
        logger.info(f"Transcribed text: {transcribed_text}")
        
        # Step 2: Extract product information
        product_info = await ai_client.extract_product_info(transcribed_text, request.language)
        logger.info(f"Extracted product info: {product_info}")
        
        # Step 3: Generate AI suggestions
        ai_suggestions = await ai_client.generate_suggestions(
            product_info, 
            transcribed_text, 
            request.language
        )
        logger.info(f"Generated AI suggestions: {ai_suggestions}")
        
        # Step 4: Store in Supabase
        stored_product = await supabase_client.store_product(
            product_info=product_info,
            ai_suggestions=ai_suggestions,
            transcribed_text=transcribed_text,
            language=request.language,
            farmer_mobile=request.farmer_mobile or "demo"
        )
        
        # Step 5: Return complete response
        response_data = {
            "success": True,
            "transcribed_text": transcribed_text,
            "product": product_info.get("product", ""),
            "quantity": product_info.get("quantity", ""),
            "price": product_info.get("price", ""),
            "description": ai_suggestions.get("description", ""),
            "suggested_price_range": ai_suggestions.get("price_range", ""),
            "market_suggestion": ai_suggestions.get("where_to_sell", ""),
            "selling_tip": ai_suggestions.get("selling_tip", ""),
            "product_id": stored_product.get("id"),
            "language": request.language
        }
        
        logger.info("Voice processing completed successfully")
        return response_data
        
    except Exception as e:
        logger.error(f"Error in complete voice process: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/api/register")
async def register_farmer(farmer: FarmerCreate):
    """Register a new farmer"""
    try:
        result = await supabase_client.register_farmer(farmer.dict())
        return {"success": True, "message": "Farmer registered successfully", "user": result}
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
async def login_farmer(credentials: Dict[str, str]):
    """Login farmer"""
    try:
        result = await supabase_client.login_farmer(credentials)
        return {"success": True, "message": "Login successful", "user": result}
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/store-product")
async def store_product(product_data: Dict[str, Any]):
    """Store product information"""
    try:
        result = await supabase_client.store_product(
            product_info=product_data.get("product_info", {}),
            ai_suggestions=product_data.get("ai_response", {}),
            transcribed_text=product_data.get("transcribed_text", ""),
            language=product_data.get("language", "en"),
            farmer_mobile=product_data.get("farmer_mobile", "demo"),
            audio_url=product_data.get("audio_url")
        )
        return {"success": True, "message": "Product stored successfully", "product_id": result.get("id")}
    except Exception as e:
        logger.error(f"Store product error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check-status")
async def check_product_status(request: Dict[str, str]):
    """Check product status by mobile number"""
    try:
        products = await supabase_client.get_products_by_mobile(request.get("mobile", ""))
        return {"success": True, "products": products}
    except Exception as e:
        logger.error(f"Check status error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/update-product-status")
async def update_product_status(product_id: str, status: str):
    """Update product status (sold/pending)"""
    try:
        result = await supabase_client.update_product_status(product_id, status)
        return {"success": True, "message": "Status updated successfully"}
    except Exception as e:
        logger.error(f"Update status error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task for unsold product suggestions
@app.post("/api/check-unsold-products")
async def check_unsold_products(background_tasks: BackgroundTasks):
    """Check for unsold products and generate improvement suggestions"""
    try:
        # Get unsold products older than 7 days
        unsold_products = await supabase_client.get_unsold_products(days=7)
        
        for product in unsold_products:
            background_tasks.add_task(
                generate_improvement_suggestions,
                product["id"],
                product["product_info"],
                product["language"]
            )
        
        return {"success": True, "message": f"Processing {len(unsold_products)} unsold products"}
    except Exception as e:
        logger.error(f"Check unsold products error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_improvement_suggestions(product_id: str, product_info: Dict, language: str):
    """Generate improvement suggestions for unsold products"""
    try:
        suggestions = await ai_client.generate_improvement_suggestions(product_info, language)
        await supabase_client.update_product_suggestions(product_id, suggestions)
        logger.info(f"Generated improvement suggestions for product {product_id}")
    except Exception as e:
        logger.error(f"Error generating improvement suggestions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 