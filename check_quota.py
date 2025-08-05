#!/usr/bin/env python3
import requests
import json
from datetime import datetime

API_KEY = "AIzaSyAauJ-z4F0fvc8-bh6iuVZzEAlGku0Jy58"

def check_quota():
    """Check current API quota and usage"""
    print("🔍 Checking Gemini API Quota...")
    print("=" * 50)
    
    # Test basic API access
    try:
        response = requests.get(f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}")
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ API Key Status: ACTIVE")
            print(f"📊 Available Models: {len(models)}")
            print(f"🆓 Account Type: FREE TIER")
            
            # Test a simple generation to check quota
            test_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-8b:generateContent"
            test_payload = {
                "contents": [{"parts": [{"text": "Hello"}]}]
            }
            
            test_response = requests.post(
                test_url, 
                headers={"Content-Type": "application/json"},
                params={"key": API_KEY},
                json=test_payload
            )
            
            if test_response.status_code == 200:
                print("✅ Generation Test: PASSED")
                print("🎯 Quota Status: AVAILABLE")
            elif test_response.status_code == 429:
                print("⚠️ Generation Test: RATE LIMITED")
                print("🚫 Quota Status: EXCEEDED")
            elif test_response.status_code == 503:
                print("🔄 Generation Test: SERVICE OVERLOADED")
                print("⏳ Quota Status: TEMPORARILY UNAVAILABLE")
            else:
                print(f"❌ Generation Test: ERROR {test_response.status_code}")
                
        elif response.status_code == 403:
            print("❌ API Key Status: INVALID or EXPIRED")
            print("🔑 Please check your API key")
        else:
            print(f"❌ API Status: ERROR {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📋 FREE TIER LIMITS:")
    print("• 15 requests per minute")
    print("• 1,500 requests per day")
    print("• 1 million tokens per day")
    print("\n💡 TIPS:")
    print("• Use shorter prompts to save tokens")
    print("• Add delays between requests")
    print("• Consider upgrading if you need more")

def estimate_usage():
    """Estimate your typical usage"""
    print("\n🧮 Usage Estimation:")
    print("-" * 30)
    
    # Estimate based on typical interview questions
    avg_question_tokens = 50  # Average question length
    avg_answer_tokens = 200   # Average answer length
    
    questions_per_session = 10
    sessions_per_day = 5
    
    daily_tokens = (avg_question_tokens + avg_answer_tokens) * questions_per_session * sessions_per_day
    
    print(f"📝 Average Question: {avg_question_tokens} tokens")
    print(f"💬 Average Answer: {avg_answer_tokens} tokens")
    print(f"🎯 Questions per Session: {questions_per_session}")
    print(f"📅 Sessions per Day: {sessions_per_day}")
    print(f"📊 Daily Token Usage: {daily_tokens:,} tokens")
    
    free_limit = 1_000_000
    percentage_used = (daily_tokens / free_limit) * 100
    
    print(f"🆓 Free Tier Limit: {free_limit:,} tokens")
    print(f"📈 Usage Percentage: {percentage_used:.1f}%")
    
    if percentage_used < 50:
        print("✅ You're well within free limits!")
    elif percentage_used < 90:
        print("⚠️ You're using most of your free quota")
    else:
        print("🚫 You may exceed free limits")

if __name__ == "__main__":
    check_quota()
    estimate_usage()
