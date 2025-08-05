#!/usr/bin/env python3
import asyncio
import json
from main import ask

class MockRequest:
    def __init__(self, data):
        self.data = data
    
    async def json(self):
        return self.data

async def test_ask_function():
    print("🧪 Testing the ask function...")
    
    # Test with a simple question
    request = MockRequest({"question": "What is Python?"})
    
    try:
        result = await ask(request)
        print(f"✅ Test passed!")
        print(f"📝 Question: What is Python?")
        print(f"💬 Answer: {result['answer'][:100]}...")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_ask_function())
