from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.qdrant_setup import (
    create_merchant_collection,
    get_collection_info,
    get_collection_stats,
    batch_upsert_vectors,
    search_vectors,
    delete_collection,
    validate_collection,
    get_collection_name
)
from uuid import uuid4

from app.services.llm_client import get_embedding

router = APIRouter()


# Pydantic models for request/response
class CreateCollectionRequest(BaseModel):
    merchant_id: str


class UpsertTestRequest(BaseModel):
    merchant_id: str
    object_type: str  # product, faq, transaction_summary, risk_assessment
    object_id: str
    text: str


class SearchTestRequest(BaseModel):
    merchant_id: str
    query: str
    object_type: Optional[str] = None
    limit: int = 5
    score_threshold: Optional[float] = None


class BatchUpsertRequest(BaseModel):
    merchant_id: str
    items: List[dict]  # Each item: {object_type, object_id, text}


@router.post("/create")
async def create_collection(request: CreateCollectionRequest):
    """Create a collection for a merchant"""
    result = create_merchant_collection(request.merchant_id)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail="Failed to create collection")
    
    return result


@router.get("/info/{merchant_id}")
async def get_info(merchant_id: str):
    """Get information about a merchant's collection"""
    info = get_collection_info(merchant_id)
    
    if not info:
        raise HTTPException(
            status_code=404,
            detail=f"Collection not found for merchant: {merchant_id}"
        )
    
    return info


@router.get("/stats/{merchant_id}")
async def get_stats(merchant_id: str):
    """Get statistics about a merchant's collection"""
    stats = get_collection_stats(merchant_id)
    
    if "error" in stats:
        raise HTTPException(status_code=404, detail=stats["error"])
    
    return stats


@router.post("/test-upsert")
async def test_upsert(request: UpsertTestRequest):
    """Test upserting a single vector to a collection"""
    # Generate embedding from text
    embedding = await get_embedding(request.text)
    
    # Prepare point data
    points = [{
    "id": str(uuid4()),  # <<< gunakan UUID valid
    "vector": embedding,
    "payload": {
        "merchant_id": request.merchant_id,
        "object_type": request.object_type,
        "object_id": request.object_id,  # ini tetap string bebas
        "text": request.text
    }
}]

    
    # Upsert
    result = batch_upsert_vectors(request.merchant_id, points)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Upsert failed"))
    
    return {
        **result,
        "object_type": request.object_type,
        "object_id": request.object_id
    }


@router.post("/test-search")
async def test_search(request: SearchTestRequest):
    """Test searching vectors in a collection"""
    # Generate query embedding
    query_embedding = await get_embedding(request.query)
    
    # Search
    results = search_vectors(
        merchant_id=request.merchant_id,
        query_vector=query_embedding,
        limit=request.limit,
        object_type=request.object_type,
        score_threshold=request.score_threshold
    )
    
    return {
        "query": request.query,
        "merchant_id": request.merchant_id,
        "object_type": request.object_type,
        "results_count": len(results),
        "results": results
    }


@router.post("/batch-upsert")
async def batch_upsert(request: BatchUpsertRequest):
    """Batch upsert multiple items to a merchant's collection"""
    # Generate embeddings for all items
    points = []
    for item in request.items:
        embedding = await get_embedding(item["text"])
        points.append({
            "id": item["object_id"],
            "vector": embedding,
            "payload": {
                "merchant_id": request.merchant_id,
                "object_type": item["object_type"],
                "object_id": item["object_id"],
                "text": item["text"]
            }
        })
    
    # Batch upsert
    result = batch_upsert_vectors(request.merchant_id, points)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Batch upsert failed"))
    
    return result


@router.delete("/{merchant_id}")
async def delete_merchant_collection(merchant_id: str):
    """Delete a merchant's collection"""
    result = delete_collection(merchant_id)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Deletion failed"))
    
    return result


@router.get("/validate/{merchant_id}")
async def validate(merchant_id: str):
    """Validate a merchant's collection health"""
    result = validate_collection(merchant_id)
    
    if not result["valid"]:
        return {
            "valid": False,
            "error": result.get("error", "Collection validation failed"),
            "merchant_id": merchant_id
        }
    
    return result
