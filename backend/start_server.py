#!/usr/bin/env python3
"""
AgriVoice Backend Server Startup Script
Starts the FastAPI server with proper configuration
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    """Start the AgriVoice backend server"""
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print("🌾 Starting AgriVoice Backend Server...")
    print("=" * 60)
    print(f"📍 Server URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/api/health")
    print("=" * 60)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=debug,
            log_level="info" if debug else "warning"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Check if port is available or try a different port")

if __name__ == "__main__":
    main() 