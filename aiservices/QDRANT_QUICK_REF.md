# Qdrant Collection Quick Reference

## ✅ Collection Status

Your collection **`merchant_merchant-001`** already exists in Qdrant Cloud!
- **Status**: green (healthy)
- **Points**: 0 (no data yet)
- **Ready to use**: Yes

## How to Add Data

### Method 1: Using cURL

```bash
# Add a product
curl -X POST http://localhost:8000/collections/test-upsert \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_id": "merchant-001",
    "object_type": "product",
    "object_id": "prod-001",
    "text": "Roti Tawar Premium - Fresh white bread made daily"
  }'

# Add an FAQ
curl -X POST http://localhost:8000/collections/test-upsert \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_id": "merchant-001",
    "object_type": "faq",
    "object_id": "faq-001",
    "text": "Q: Store hours? A: Mon-Sat 8AM-8PM"
  }'
```

### Method 2: Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/collections/test-upsert",
    json={
        "merchant_id": "merchant-001",
        "object_type": "product",
        "object_id": "prod-001",
        "text": "Your product description here"
    }
)
print(response.json())
```

### Method 3: Test in Browser

1. Open: **http://localhost:8000/docs**
2. Find: **POST /collections/test-upsert**
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

## Check Collection Info

```bash
# Get collection information
curl http://localhost:8000/collections/info/merchant-001

# Get statistics
curl http://localhost:8000/collections/stats/merchant-001
```

## Search Your Data

```bash
curl -X POST http://localhost:8000/collections/test-search \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_id": "merchant-001",
    "query": "fresh bread",
    "limit": 5
  }'
```

## Object Types Supported

- `product` - Product catalog items
- `faq` - Frequently asked questions
- `transaction_summary` - Transaction insights
- `risk_assessment` - Risk data

## Troubleshooting

### If you get "Collection doesn't exist"
Run: `python create_qdrant_collection_direct.py`

### If embeddings fail
Check your OpenAI API key in `.env`:
```
OPENAI_API_KEY=sk-proj-...
```

### View all collections
```python
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collections = client.get_collections()
for c in collections.collections:
    print(f"- {c.name}")
```
