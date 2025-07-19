#!/usr/bin/env python3
"""
AgriVoice - Simple Startup Script
Run this to start the AgriVoice application
"""

import subprocess
import sys
import os

def main():
    print("🌾 AgriVoice - Voice-based Product Catalog")
    print("=" * 50)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed!")
    except subprocess.CalledProcessError:
        print("⚠️  Some dependencies may not have installed properly")
    
    # Start the server
    print("\n🚀 Starting AgriVoice API server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    print("\n" + "="*50)
    
    # Change to backend directory and start server
    os.chdir("backend")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    main() 