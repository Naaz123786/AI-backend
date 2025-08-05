#!/usr/bin/env python3
import requests
import json
import time

def test_api():
    # Test the API endpoint
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": "What is Python programming language?"}]}]
    }
    params = {"key": "AIzaSyAauJ-z4F0fvc8-bh6iuVZzEAlGku0Jy58"}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ Success! Answer: {answer[:100]}...")
                return True
            else:
                print(f"❌ Error: Unexpected response format")
                return False
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    test_api()
