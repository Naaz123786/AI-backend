#!/usr/bin/env python3
import requests
import json
import time

def test_server():
    # Test the FastAPI server
    url = "http://127.0.0.1:8000/ask"
    headers = {"Content-Type": "application/json"}
    payload = {
        "question": "What is Python programming language?"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "answer" in result:
                answer = result["answer"]
                print(f"✅ Success! Answer: {answer[:150]}...")
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
    print("Testing FastAPI server...")
    test_server()
