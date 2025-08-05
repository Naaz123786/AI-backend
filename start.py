#!/usr/bin/env python3
"""
Startup script for Render deployment
"""
import os
import sys

def main():
    # Debug info
    print("🔍 Python version:", sys.version)
    print("🔍 Python path:", sys.path)
    print("🔍 Current directory:", os.getcwd())
    print("🔍 Environment PORT:", os.environ.get("PORT", "Not set"))
    
    # Import and run
    try:
        from app import app
        import uvicorn
        
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        
        print(f"🚀 Starting uvicorn on {host}:{port}")
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=1,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
