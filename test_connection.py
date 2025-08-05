#!/usr/bin/env python3
import requests
import time
import subprocess
import sys

def test_backend():
    """Test if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running on port 8000")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running on port 8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Backend is taking too long to respond")
        return False

def test_frontend():
    """Test if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running on port 3000")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running on port 3000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Frontend is taking too long to respond")
        return False

def test_api_endpoint():
    """Test the API endpoint"""
    try:
        payload = {"question": "What is Python?"}
        response = requests.post("http://127.0.0.1:8000/ask", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "answer" in data:
                print("✅ API endpoint is working")
                print(f"📝 Sample response: {data['answer'][:100]}...")
                return True
            else:
                print("❌ API returned unexpected format")
                return False
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API endpoint")
        return False
    except requests.exceptions.Timeout:
        print("❌ API request timed out")
        return False

def main():
    print("🧪 Testing AI Interview Assistant Connection...")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend()
    time.sleep(1)
    
    # Test frontend
    frontend_ok = test_frontend()
    time.sleep(1)
    
    # Test API endpoint
    api_ok = test_api_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"Backend: {'✅ OK' if backend_ok else '❌ Failed'}")
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ Failed'}")
    print(f"API: {'✅ OK' if api_ok else '❌ Failed'}")
    
    if backend_ok and frontend_ok and api_ok:
        print("\n🎉 All systems are working! Your app is ready to use.")
        print("🌐 Open http://localhost:3000 in your browser")
    else:
        print("\n🔧 Some issues found. Please check:")
        if not backend_ok:
            print("   - Start the backend server: cd backend && python -m uvicorn main:app --reload --port 8000")
        if not frontend_ok:
            print("   - Start the frontend server: cd frontend && npm run dev")
        if not api_ok:
            print("   - Check if both servers are running")

if __name__ == "__main__":
    main()
