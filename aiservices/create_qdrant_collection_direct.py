"""
Create Qdrant collection directly using Qdrant client (bypass FastAPI)
"""
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials from .env
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print("="*60)
print("DIRECT QDRANT COLLECTION CREATION")
print("="*60)

# Connect to Qdrant
print(f"\n1. Connecting to Qdrant Cloud...")
print(f"   URL: {qdrant_url[:50]}...")

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)
print("   ✅ Connected!")

# Create collection
merchant_id = "merchant-001"
collection_name = f"merchant_{merchant_id}"

print(f"\n2. Creating collection '{collection_name}'...")

try:
    # Check if exists
    collections = client.get_collections()
    existing = [c.name for c in collections.collections]
    
    if collection_name in existing:
        print(f"   ⚠️  Collection already exists!")
        info = client.get_collection(collection_name)
        print(f"   Points: {info.points_count}")
        print(f"   Status: {info.status}")
    else:
        # Create new
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # OpenAI text-embedding-3-small dimension
                distance=Distance.COSINE
            )
        )
        print(f"   ✅ Collection created successfully!")
        
        # Verify
        info = client.get_collection(collection_name)
        print(f"   Status: {info.status}")
        print(f"   Vector size: {info.config.params.vectors.size}")
        print(f"   Distance: {info.config.params.vectors.distance}")

except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ DONE!")
print("="*60)
print(f"\nCollection '{collection_name}' is ready in Qdrant Cloud.")
print(f"\nNow you can add embeddings via:")
print(f"- FastAPI endpoint: POST /collections/test-upsert")
print(f"- Or use the embeddings router: POST /embeddings/upsert")
