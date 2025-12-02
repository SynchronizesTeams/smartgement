from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.qdrant_setup import client, create_collection_if_not_exists, get_collection_name
from app.services.llm_client import get_embedding

router = APIRouter()


class UpsertEmbeddingRequest(BaseModel):
    merchant_id: str
    text: str
    object_id: str
    object_type: str  # product, faq, transaction_summary, risk_assessment
    metadata: Optional[dict] = None


@router.post("/upsert")
async def upsert_vector(body: UpsertEmbeddingRequest):
    """Upsert a single embedding to merchant's collection"""
    merchant_id = body.merchant_id
    text = body.text
    object_id = body.object_id
    object_type = body.object_type

    collection = get_collection_name(merchant_id)
    create_collection_if_not_exists(collection)

    embedding = await get_embedding(text)
    
    # Build payload with metadata
    payload = {
        "merchant_id": merchant_id,
        "object_id": object_id,
        "object_type": object_type,
        "text": text  # Store text for context retrieval
    }
    
    # Add additional metadata if provided
    if body.metadata:
        payload.update(body.metadata)

    client.upsert(
        collection_name=collection,
        points=[{
            "id": object_id,
            "vector": embedding,
            "payload": payload
        }]
    )

    return {
        "status": "ok",
        "collection": collection,
        "object_type": object_type,
        "object_id": object_id
    }

