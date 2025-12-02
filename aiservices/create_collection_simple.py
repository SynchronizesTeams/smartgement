"""
Simple collection creation without embeddings (just create the structure)
"""
import requests

BASE_URL = "http://localhost:8000"
merchant_id = "merchant-001"

print("Creating Qdrant collection...")
response = requests.post(
    f"{BASE_URL}/collections/create",
    json={"merchant_id": merchant_id}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    print(f"\n✅ Success! Collection created: merchant_{merchant_id}")
    print(f"\nTo view info:")
    print(f"GET {BASE_URL}/collections/info/{merchant_id}")
    print(f"\nTo add data:")
    print(f"POST {BASE_URL}/collections/test-upsert")
    print(f"Body: {{'merchant_id': '{merchant_id}', 'object_type': 'product', 'object_id': 'prod-1', 'text': 'Your product description'}}")
