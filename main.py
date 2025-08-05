from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests
import time
import random
import json
import asyncio

load_dotenv()

app = FastAPI()

# CORS configuration for production (Render + Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "https://*.vercel.app",
        "https://your-app-name.vercel.app",  # Replace with your actual Vercel URL
        "*"  # Remove this in production and add specific domains
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Fallback models in order of preference
FALLBACK_MODELS = [
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-8b-001", 
    "gemini-2.5-flash",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro"
]

def call_gemini_with_retry(url, headers, params, payload, max_retries=3):
    """Call Gemini API with retry logic for rate limiting"""
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, params=params, json=payload)
            
            if response.status_code == 429:  # Rate limit exceeded
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
                    print(f"Rate limit hit, waiting {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {"error": "Rate limit exceeded. Please try again later."}
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Request failed, retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                return {"error": f"Request failed after {max_retries} attempts: {str(e)}"}
    
    return {"error": "Max retries exceeded"}

def try_gemini_with_fallback(prompt):
    """Try different Gemini models until one works"""
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    params = {"key": GEMINI_API_KEY}
    
    for model in FALLBACK_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"
        print(f"Trying model: {model}")
        
        result = call_gemini_with_retry(url, headers, params, payload)
        
        if "error" not in result:
            print(f"✅ Success with model: {model}")
            return result
        else:
            print(f"❌ Failed with model: {model} - {result['error']}")
    
    return {"error": "All models failed. Please try again later."}

@app.get("/")
async def root():
    return {"message": "AI Interview Assistant Backend is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-interview-backend"}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    if not question:
        return {"answer": "Please provide a question."}
    try:
        prompt = (
            "You are a professional interview assistant in CONTINUOUS MODE. "
            "Your job is to help the user answer interview questions in a clear, point-by-point format. "
            "IMPORTANT: Always structure your answer in numbered points (1., 2., 3., etc.). "
            "Each point should be on a NEW LINE and be one clear sentence or concept. "
            "Start each point with a number followed by a period and space (like '1. ', '2. ', '3. '). "
            "If the question is technical, provide step-by-step explanation in numbered points. "
            "If the question is HR/behavioral, give a structured answer using numbered points (like STAR method). "
            "Keep each point concise and easy to understand. "
            "Maximum 6 points per answer. "
            "After providing the answer, the system will automatically clear this question and listen for the next one. "
            "Format example:\n1. First point here\n2. Second point here\n3. Third point here\n\n"
            f"Question: {question}\n\n"
            "Answer (in numbered points):"
        )
        # Use fallback system
        result = try_gemini_with_fallback(prompt)
        
        if "error" in result:
            return {"answer": f"Error: {result['error']}"}

        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "question":
                question = message.get("question", "")
                if question:
                    # Generate AI response
                    prompt = (
                        "You are a professional interview assistant in CONTINUOUS LIVE MODE. "
                        "Your job is to help the user answer interview questions in a clear, point-by-point format. "
                        "IMPORTANT: Always structure your answer in numbered points (1., 2., 3., etc.). "
                        "Each point should be on a NEW LINE and be one clear sentence or concept. "
                        "Start each point with a number followed by a period and space (like '1. ', '2. ', '3. '). "
                        "If the question is technical, provide step-by-step explanation in numbered points. "
                        "If the question is HR/behavioral, give a structured answer using numbered points (like STAR method). "
                        "Keep each point concise and easy to understand. "
                        "Maximum 6 points per answer. "
                        "After providing the answer, the system will automatically clear this question and listen for the next one. "
                        "Format example:\n1. First point here\n2. Second point here\n3. Third point here\n\n"
                        f"Question: {question}\n\n"
                        "Answer (in numbered points):"
                    )
                    
                    # Use fallback system
                    result = try_gemini_with_fallback(prompt)
                    
                    if "error" in result:
                        answer = f"Error: {result['error']}"
                    else:
                        answer = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Send response back to client
                    response = {
                        "type": "answer",
                        "answer": answer
                    }
                    await manager.send_personal_message(json.dumps(response), websocket)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
