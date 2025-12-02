"""
Simple manual test to verify collections endpoint
"""
import requests

# Test if collections endpoint exists
try:
    response = requests.post(
        "http://localhost:8000/collections/create",
        json={"merchant_id": "test-001"}
    )
    print(f"Create collection status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test info endpoint
try:
    response = requests.get("http://localhost:8000/collections/info/test-001")
    print(f"\nInfo status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test swagger docs to see if endpoint is registered
try:
    response = requests.get("http://localhost:8000/docs")
    print(f"\nSwagger docs accessible: {response.status_code == 200}")
except Exception as e:
    print(f"Error accessing docs: {e}")
