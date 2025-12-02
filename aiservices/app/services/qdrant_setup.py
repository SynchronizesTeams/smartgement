from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from app.config import settings
from typing import List, Dict, Optional
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

# Initialize Qdrant client with credentials from config
client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key
)

def get_collection_name(merchant_id: str) -> str:
    """Generate standardized collection name for merchant"""
    return f"merchant_{merchant_id}"


def create_collection_if_not_exists(name: str) -> bool:
    """Create a Qdrant collection if it doesn't exist"""
    try:
        existing_collections = [c.name for c in client.get_collections().collections]
        if name not in existing_collections:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=settings.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection: {name}")
        return True
    except Exception as e:
        logger.error(f"Error creating collection {name}: {e}")
        return False


def create_merchant_collection(merchant_id: str) -> Dict:
    """Create a collection for a specific merchant"""
    collection_name = get_collection_name(merchant_id)
    success = create_collection_if_not_exists(collection_name)
    
    return {
        "success": success,
        "collection_name": collection_name,
        "merchant_id": merchant_id
    }


def get_collection_info(merchant_id: str) -> Optional[Dict]:
    """Get information about a merchant's collection"""
    collection_name = get_collection_name(merchant_id)
    
    try:
        collection_info = client.get_collection(collection_name)
        return {
            "collection_name": collection_name,
            "merchant_id": merchant_id,
            "vectors_count": collection_info.vectors_count,
            "points_count": collection_info.points_count,
            "status": collection_info.status,
            "config": {
                "size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance
            }
        }
    except Exception as e:
        logger.error(f"Error getting collection info for {collection_name}: {e}")
        return None


def get_collection_stats(merchant_id: str) -> Dict:
    """Get statistics about embeddings in a merchant's collection"""
    collection_name = get_collection_name(merchant_id)
    
    try:
        # Get collection info
        info = get_collection_info(merchant_id)
        if not info:
            return {"error": "Collection not found"}
        
        # Count by object type
        object_types = ["product", "faq", "transaction_summary", "risk_assessment"]
        type_counts = {}
        
        for obj_type in object_types:
            # Scroll through points to count by type
            # Note: In production, you might want to use scroll with filter
            type_counts[obj_type] = 0
        
        return {
            "collection_name": collection_name,
            "merchant_id": merchant_id,
            "total_points": info["points_count"],
            "total_vectors": info["vectors_count"],
            "by_type": type_counts,
            "status": "active"
        }
    except Exception as e:
        logger.error(f"Error getting stats for {collection_name}: {e}")
        return {"error": str(e)}


def batch_upsert_vectors(
    merchant_id: str,
    points: List[Dict]
) -> Dict:
    """
    Batch upsert multiple vectors to a merchant's collection
    
    Args:
        merchant_id: Merchant identifier
        points: List of dicts with keys: id, vector, payload
    """
    collection_name = get_collection_name(merchant_id)
    
    try:
        # Ensure collection exists
        create_collection_if_not_exists(collection_name)
        
        # Convert to PointStruct objects
        point_structs = [
            PointStruct(
                id=point.get("id", str(uuid4())),
                vector=point["vector"],
                payload=point.get("payload", {})
            )
            for point in points
        ]
        
        # Upsert batch
        client.upsert(
            collection_name=collection_name,
            points=point_structs
        )
        
        return {
            "success": True,
            "collection_name": collection_name,
            "upserted_count": len(point_structs)
        }
    except Exception as e:
        logger.error(f"Error batch upserting to {collection_name}: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def search_vectors(
    merchant_id: str,
    query_vector: List[float],
    limit: int = 5,
    object_type: Optional[str] = None,
    score_threshold: Optional[float] = None
) -> List[Dict]:
    """
    Search for similar vectors in a merchant's collection
    
    Args:
        merchant_id: Merchant identifier
        query_vector: Query embedding vector
        limit: Maximum number of results
        object_type: Filter by object type (product, faq, etc.)
        score_threshold: Minimum similarity score
    """
    collection_name = get_collection_name(merchant_id)
    
    try:
        # Build filter if object_type specified
        query_filter = None
        if object_type:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="object_type",
                        match=MatchValue(value=object_type)
                    )
                ]
            )
        
        # Search using the correct Qdrant API
        search_result = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            query_filter=query_filter,
            score_threshold=score_threshold
        )
        
        # Format results
        results = []
        for hit in search_result.points:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            })
        
        return results
    except Exception as e:
        logger.error(f"Error searching {collection_name}: {e}")
        return []


def delete_collection(merchant_id: str) -> Dict:
    """Delete a merchant's collection"""
    collection_name = get_collection_name(merchant_id)
    
    try:
        client.delete_collection(collection_name)
        return {
            "success": True,
            "collection_name": collection_name,
            "message": f"Collection {collection_name} deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting {collection_name}: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def validate_collection(merchant_id: str) -> Dict:
    """Validate that a merchant's collection is healthy"""
    collection_name = get_collection_name(merchant_id)
    
    try:
        info = get_collection_info(merchant_id)
        if not info:
            return {
                "valid": False,
                "error": "Collection does not exist"
            }
        
        # Check if collection is ready
        is_valid = info["status"] == "green"
        
        return {
            "valid": is_valid,
            "collection_name": collection_name,
            "status": info["status"],
            "points_count": info["points_count"]
        }
    except Exception as e:
        logger.error(f"Error validating {collection_name}: {e}")
        return {
            "valid": False,
            "error": str(e)
        }
