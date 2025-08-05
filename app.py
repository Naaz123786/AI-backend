#!/usr/bin/env python3
"""
Entry point for Render deployment - ASGI compatible
"""
import os
from main import app

# Export app for ASGI servers (gunicorn, uvicorn)
# This makes the app accessible as 'app:app'
__all__ = ['app']

# Set host and port for Render
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server for Render...")
    print(f"📡 Server will run on: {HOST}:{PORT}")
    print(f"📝 API endpoint: http://{HOST}:{PORT}/ask")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
        workers=1,
        log_level="info"
    )
