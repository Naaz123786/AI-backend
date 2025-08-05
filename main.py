# Import FastAPI app from app.py
from app import app

# This allows gunicorn to access the app as 'main:app'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
