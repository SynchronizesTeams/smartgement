"""
Test script for Qdrant multi-tenant collection service
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_collection():
    """Test creating a collection for a merchant"""
    print("\n=== Test 1: Create Collection ===")
    response = requests.post(
        f"{BASE_URL}/collections/create",
        json={"merchant_id": "test-merchant-001"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_collection_info():
    """Test getting collection info"""
    print("\n=== Test 2: Get Collection Info ===")
    response = requests.get(f"{BASE_URL}/collections/info/test-merchant-001")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_upsert_embeddings():
    """Test upserting product embeddings"""
    print("\n=== Test 3: Upsert Product Embeddings ===")
    
    test_products = [
        {
            "merchant_id": "test-merchant-001",
            "object_type": "product",
            "object_id": "prod-001",
            "text": "Roti Tawar Premium - Fresh white bread made daily with high-quality flour"
        },
        {
            "merchant_id": "test-merchant-001",
            "object_type": "product",
            "object_id": "prod-002",
            "text": "Roti Gandum Sehat - Healthy whole wheat bread, perfect for diet"
        },
        {
            "merchant_id": "test-merchant-001",
            "object_type": "faq",
            "object_id": "faq-001",
            "text": "Q: What are your store hours? A: We are open Monday to Saturday, 8 AM to 8 PM"
        }
    ]
    
    for product in test_products:
        response = requests.post(
            f"{BASE_URL}/collections/test-upsert",
            json=product
        )
        print(f"Upserted {product['object_type']} {product['object_id']}: {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
    
    return True


def test_search():
    """Test semantic search"""
    print("\n=== Test 4: Semantic Search ===")
    
    # Test 1: Search for bread products
    print("\nSearch 1: 'fresh bread products'")
    response = requests.post(
        f"{BASE_URL}/collections/test-search",
        json={
            "merchant_id": "test-merchant-001",
            "query": "fresh bread products",
            "object_type": "product",
            "limit": 5
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['results_count']} results:")
        for result in data['results']:
            print(f"  - ID: {result['id']}, Score: {result['score']:.4f}")
            print(f"    Text: {result['payload'].get('text', 'N/A')[:80]}...")
    
    # Test 2: Search all types
    print("\nSearch 2: 'store information' (all types)")
    response = requests.post(
        f"{BASE_URL}/collections/test-search",
        json={
            "merchant_id": "test-merchant-001",
            "query": "store hours and information",
            "limit": 5
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['results_count']} results:")
        for result in data['results']:
            print(f"  - Type: {result['payload'].get('object_type')}, Score: {result['score']:.4f}")
    
    return True


def test_collection_stats():
    """Test getting collection statistics"""
    print("\n=== Test 5: Collection Statistics ===")
    response = requests.get(f"{BASE_URL}/collections/stats/test-merchant-001")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_chatbot_with_context():
    """Test chatbot with merchant context"""
    print("\n=== Test 6: Chatbot with Dynamic Context ===")
    response = requests.post(
        f"{BASE_URL}/chatbot/message",
        json={
            "merchant_id": "test-merchant-001",
            "message": "Apa produk roti yang kita punya?"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Intent: {data.get('intent')}, Confidence: {data.get('confidence')}")
        print(f"Response: {data.get('response')}")
        print(f"Suggested Actions: {data.get('suggested_actions')}")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("QDRANT MULTI-TENANT COLLECTION SERVICE TESTS")
    print("=" * 60)
    
    try:
        test_create_collection()
        test_collection_info()
        test_upsert_embeddings()
        test_search()
        test_collection_stats()
        test_chatbot_with_context()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
