"""
Qdrant Connection Diagnostic Script
Test if Qdrant Cloud credentials are working
"""
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("QDRANT CLOUD CONNECTION DIAGNOSTIC")
print("=" * 60)

# Get credentials
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print(f"\n1. Environment Variables:")
print(f"   QDRANT_URL: {qdrant_url[:50]}..." if qdrant_url else "   QDRANT_URL: NOT SET")
print(f"   QDRANT_API_KEY: {qdrant_api_key[:20]}..." if qdrant_api_key else "   QDRANT_API_KEY: NOT SET")

if not qdrant_url or not qdrant_api_key:
    print("\n❌ ERROR: Missing Qdrant credentials in .env file")
    print("\nYour .env should have:")
    print("QDRANT_URL=https://your-cluster.gcp.cloud.qdrant.io")
    print("QDRANT_API_KEY=your-api-key")
    exit(1)

# Try to connect
print(f"\n2. Testing Connection...")
try:
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )
    print("   ✅ Client created successfully")
except Exception as e:
    print(f"   ❌ Failed to create client: {e}")
    exit(1)

# Try to list collections
print(f"\n3. Testing API Access (List Collections)...")
try:
    collections = client.get_collections()
    print(f"   ✅ Successfully accessed Qdrant Cloud!")
    print(f"   Existing collections: {[c.name for c in collections.collections]}")
except Exception as e:
    print(f"   ❌ Failed to access Qdrant: {e}")
    print(f"\n   Error type: {type(e).__name__}")
    print(f"   Error details: {str(e)}")
    
    if "403" in str(e) or "forbidden" in str(e).lower():
        print("\n   🔍 DIAGNOSIS: 403 Forbidden Error")
        print("   This means your API key is invalid or doesn't have permissions.")
        print("\n   SOLUTIONS:")
        print("   1. Go to Qdrant Cloud Dashboard: https://cloud.qdrant.io/")
        print("   2. Check if your cluster is running")
        print("   3. Generate a NEW API key with full permissions")
        print("   4. Update your .env file with the new key")
        print("\n   Note: API keys should look like:")
        print("   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    
    exit(1)

# Try to create a test collection
print(f"\n4. Testing Collection Creation...")
test_collection = "test_connection"
try:
    from qdrant_client.models import VectorParams, Distance
    
    # Delete if exists
    try:
        client.delete_collection(test_collection)
        print(f"   Deleted existing test collection")
    except:
        pass
    
    # Create new
    client.create_collection(
        collection_name=test_collection,
        vectors_config=VectorParams(size=128, distance=Distance.COSINE)
    )
    print(f"   ✅ Successfully created test collection '{test_collection}'")
    
    # Verify
    info = client.get_collection(test_collection)
    print(f"   Collection status: {info.status}")
    
    # Clean up
    client.delete_collection(test_collection)
    print(f"   ✅ Successfully deleted test collection")
    
except Exception as e:
    print(f"   ❌ Failed to create collection: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - QDRANT CONNECTION IS WORKING!")
print("=" * 60)
print("\nYour Qdrant Cloud setup is correctly configured.")
print("The 403 errors in your application might be from a different issue.")
