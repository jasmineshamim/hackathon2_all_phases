#!/usr/bin/env python3
"""
Quick verification script to test all critical endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8001"

print("=" * 70)
print("PHASE III TODO AI CHATBOT - ENDPOINT VERIFICATION")
print("=" * 70)

# Test 1: Health
print("\n[1/6] Testing /health endpoint...")
try:
    r = requests.get(f"{BASE_URL}/health")
    print(f"      Status: {r.status_code} - {'PASS' if r.status_code == 200 else 'FAIL'}")
except Exception as e:
    print(f"      FAIL: {e}")

# Test 2: Root
print("\n[2/6] Testing / endpoint...")
try:
    r = requests.get(f"{BASE_URL}/")
    print(f"      Status: {r.status_code} - {'PASS' if r.status_code == 200 else 'FAIL'}")
except Exception as e:
    print(f"      FAIL: {e}")

# Test 3: OpenAPI
print("\n[3/6] Testing /openapi.json endpoint...")
try:
    r = requests.get(f"{BASE_URL}/openapi.json")
    data = r.json()
    has_chat = "/api/{user_id}/chat" in data.get("paths", {})
    print(f"      Status: {r.status_code} - {'PASS' if r.status_code == 200 else 'FAIL'}")
    print(f"      Chat endpoint in schema: {'YES' if has_chat else 'NO'}")
except Exception as e:
    print(f"      FAIL: {e}")

# Test 4: Docs
print("\n[4/6] Testing /docs endpoint...")
try:
    r = requests.get(f"{BASE_URL}/docs")
    has_swagger = "swagger" in r.text.lower()
    print(f"      Status: {r.status_code} - {'PASS' if r.status_code == 200 else 'FAIL'}")
    print(f"      Swagger UI loaded: {'YES' if has_swagger else 'NO'}")
except Exception as e:
    print(f"      FAIL: {e}")

# Test 5: Register
print("\n[5/6] Testing /auth/register endpoint...")
try:
    import time
    data = {
        "email": f"verify_{int(time.time())}@test.com",
        "password": "Test123!",
        "name": "Verify User"
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"      Status: {r.status_code} - {'PASS' if r.status_code == 200 else 'FAIL'}")
    if r.status_code == 200:
        token = r.json().get("access_token")
        user_id = r.json().get("user_id")
        print(f"      Token received: {'YES' if token else 'NO'}")

        # Test 6: Chat endpoint
        print("\n[6/6] Testing /api/{user_id}/chat endpoint...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            chat_data = {"message": "Hello, create a task to test the system"}
            r = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
            print(f"      Status: {r.status_code} - {'PASS' if r.status_code == 200 else 'FAIL'}")
            if r.status_code == 200:
                resp = r.json()
                print(f"      Conversation ID: {resp.get('conversation_id')}")
                print(f"      Tool calls made: {len(resp.get('tool_calls', []))}")
        except Exception as e:
            print(f"      FAIL: {e}")
except Exception as e:
    print(f"      FAIL: {e}")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
print("\nBackend is running on: http://localhost:8001")
print("API Documentation: http://localhost:8001/docs")
print("Frontend should connect to: http://localhost:8001")
print("\nTo start frontend: cd frontend && npm run dev")
