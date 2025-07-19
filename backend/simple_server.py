#!/usr/bin/env python3
"""
Minimal working server for testing
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AgriVoice API is running! 🌾", "version": "1.0.0", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🌾 Starting minimal server...")
    uvicorn.run(app, host="127.0.0.1", port=8000) 