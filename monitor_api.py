#!/usr/bin/env python3
import requests
import time
import json
from datetime import datetime

API_KEY = "AIzaSyAauJ-z4F0fvc8-bh6iuVZzEAlGku0Jy58"

MODELS_TO_TEST = [
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-8b-001", 
    "gemini-2.5-flash",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro"
]

def test_model(model_name):
    """Test a specific model"""
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
    params = {"key": API_KEY}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=10)
        if response.status_code == 200:
            return "✅ Working"
        elif response.status_code == 503:
            return "🔄 Overloaded"
        elif response.status_code == 429:
            return "⏸️ Rate Limited"
        else:
            return f"❌ Error {response.status_code}"
    except Exception as e:
        return f"❌ Failed: {str(e)}"

def monitor_api():
    """Monitor API status"""
    print("🔍 Gemini API Status Monitor")
    print("=" * 50)
    
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n⏰ {current_time}")
        print("-" * 30)
        
        working_models = []
        
        for model in MODELS_TO_TEST:
            status = test_model(model)
            print(f"{model}: {status}")
            
            if "Working" in status:
                working_models.append(model)
        
        print(f"\n📊 Working Models: {len(working_models)}/{len(MODELS_TO_TEST)}")
        
        if working_models:
            print(f"🎯 Best Model: {working_models[0]}")
        else:
            print("⚠️ No models working!")
        
        print("\nWaiting 30 seconds for next check...")
        time.sleep(30)

if __name__ == "__main__":
    try:
        monitor_api()
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped.")
