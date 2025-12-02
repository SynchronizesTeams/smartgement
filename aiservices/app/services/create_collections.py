from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
import os
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

client.recreate_collection(
    collection_name="products",
    vectors_config=VectorParams(
        size=384,          # ukuran vector MiniLM
        distance=Distance.COSINE
    )
)

print("Collection 'products' created!")
