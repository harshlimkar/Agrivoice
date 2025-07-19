#!/usr/bin/env python3
"""
Alternative server startup script
"""

import uvicorn
import sys
import os

def start_server():
    """Start the AgriVoice server"""
    print("🌾 Starting AgriVoice API Server...")
    print("=" * 50)
    print("📱 Open http://localhost:8000 in your browser")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    print("\n" + "="*50)
    
    try:
        # Import the app
        from main import app
        
        # Start server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Trying alternative method...")
        try:
            # Alternative method
            uvicorn.run(
                "main:app",
                host="127.0.0.1",
                port=8000,
                reload=False,
                log_level="info"
            )
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")
            print("💡 Please check if port 8000 is available")

if __name__ == "__main__":
    start_server() 