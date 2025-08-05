#!/usr/bin/env python3
import uvicorn
import os
from main import app

if __name__ == "__main__":
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"  # Important: Use 0.0.0.0 for Render deployment
    
    print("🚀 Starting FastAPI server for Render...")
    print(f"📡 Server will run on: {host}:{port}")
    print(f"📝 API endpoint: http://{host}:{port}/ask")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        # Use reload=False for production
        uvicorn.run(
            app, 
            host=host, 
            port=port, 
            reload=False,
            workers=1,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")
