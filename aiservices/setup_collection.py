"""
Quick script to create a Qdrant collection and add sample data
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def create_collection_and_add_data():
    """Create collection and add sample product/FAQ data"""
    
    # Step 1: Create collection for test merchant
    print("Step 1: Creating collection...")
    merchant_id = "merchant-001"
    
    response = requests.post(
        f"{BASE_URL}/collections/create",
        json={"merchant_id": merchant_id}
    )
    
    if response.status_code == 200:
        print(f"✅ Collection created: {response.json()}")
    else:
        print(f"⚠️ Collection creation response: {response.status_code}")
        print(response.json())
    
    # Step 2: Add sample products
    print("\nStep 2: Adding sample products...")
    
    sample_data = [
        {
            "merchant_id": merchant_id,
            "object_type": "product",
            "object_id": "prod-001",
            "text": "Roti Tawar Premium - Fresh white bread made daily with high-quality flour. Perfect for breakfast sandwiches."
        },
        {
            "merchant_id": merchant_id,
            "object_type": "product",
            "object_id": "prod-002",
            "text": "Roti Gandum Sehat - Healthy whole wheat bread, rich in fiber. Perfect for diet and healthy lifestyle."
        },
        {
            "merchant_id": merchant_id,
            "object_type": "product",
            "object_id": "prod-003",
            "text": "Kue Brownies Coklat - Rich chocolate brownies with premium cocoa. Moist and delicious."
        },
        {
            "merchant_id": merchant_id,
            "object_type": "faq",
            "object_id": "faq-001",
            "text": "Q: What are your store hours? A: We are open Monday to Saturday, 8 AM to 8 PM. Closed on Sundays."
        },
        {
            "merchant_id": merchant_id,
            "object_type": "faq",
            "object_id": "faq-002",
            "text": "Q: Do you deliver? A: Yes, we deliver within 5km radius. Free delivery for orders above 100k."
        }
    ]
    
    for item in sample_data:
        response = requests.post(
            f"{BASE_URL}/collections/test-upsert",
            json=item
        )
        
        if response.status_code == 200:
            print(f"✅ Added {item['object_type']}: {item['object_id']}")
        else:
            print(f"❌ Failed to add {item['object_id']}: {response.status_code}")
            print(response.json())
    
    # Step 3: Verify collection
    print("\nStep 3: Verifying collection...")
    response = requests.get(f"{BASE_URL}/collections/info/{merchant_id}")
    
    if response.status_code == 200:
        info = response.json()
        print(f"✅ Collection verified!")
        print(f"   - Name: {info['collection_name']}")
        print(f"   - Points: {info['points_count']}")
        print(f"   - Status: {info['status']}")
    else:
        print(f"❌ Failed to verify: {response.status_code}")
    
    # Step 4: Test search
    print("\nStep 4: Testing semantic search...")
    response = requests.post(
        f"{BASE_URL}/collections/test-search",
        json={
            "merchant_id": merchant_id,
            "query": "healthy bread products",
            "limit": 3
        }
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Search works! Found {results['results_count']} results:")
        for result in results['results']:
            text = result['payload'].get('text', '')[:60]
            print(f"   - {text}... (score: {result['score']:.3f})")
    
    print("\n" + "="*60)
    print(f"✅ DONE! Collection '{merchant_id}' is ready to use!")
    print("="*60)
    print(f"\nYou can now:")
    print(f"1. Test chatbot: POST {BASE_URL}/chatbot/message")
    print(f"   with {{'merchant_id': '{merchant_id}', 'message': 'What products do we have?'}}")
    print(f"2. View docs: http://localhost:8000/docs")
    print(f"3. Add more data using /collections/test-upsert endpoint")

if __name__ == "__main__":
    print("="*60)
    print("QDRANT COLLECTION SETUP")
    print("="*60)
    print()
    
    try:
        create_collection_and_add_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
