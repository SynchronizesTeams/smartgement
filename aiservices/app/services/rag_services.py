from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.services.qdrant_setup import client, get_collection_name, search_vectors
from app.services.llm_client import generate_text, get_embedding
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


async def rag_answer(
    merchant_id: str,
    query: str,
    object_types: Optional[List[str]] = None,
    limit: int = 5
):
    """
    Answer a query using RAG (Retrieval-Augmented Generation)
    
    Args:
        merchant_id: Merchant identifier
        query: User's question
        object_types: Optional list of object types to search (product, faq, etc.)
        limit: Number of similar items to retrieve
    """
    collection = get_collection_name(merchant_id)
    
    try:
        # Generate query embedding
        query_emb = await get_embedding(query)
        
        # Search for relevant context
        # If object_types specified, search each type separately
        all_results = []
        
        if object_types:
            for obj_type in object_types:
                results = search_vectors(
                    merchant_id=merchant_id,
                    query_vector=query_emb,
                    limit=limit,
                    object_type=obj_type
                )
                all_results.extend(results)
        else:
            # Search all types
            all_results = search_vectors(
                merchant_id=merchant_id,
                query_vector=query_emb,
                limit=limit
            )
        
        # Build context from search results
        if not all_results:
            return "Maaf, saya tidak memiliki cukup informasi untuk menjawab pertanyaan tersebut. Silakan tambahkan lebih banyak data produk atau informasi bisnis."
        
        context_parts = []
        for idx, result in enumerate(all_results[:limit], 1):
            payload = result.get("payload", {})
            text = payload.get("text", "")
            obj_type = payload.get("object_type", "unknown")
            score = result.get("score", 0)
            
            if text:
                context_parts.append(f"[{obj_type.upper()}] (relevance: {score:.2f})\n{text}")
        
        context = "\n\n".join(context_parts)
        
        # Generate system prompt with context
        system_prompt = f"""You are an AI assistant for a merchant's business.
Use the following context from the merchant's database to answer questions accurately.
If the context doesn't contain relevant information, say so honestly.

Context:
{context}
"""
        
        # Generate answer
        answer = await generate_text(
            prompt=query,
            system_prompt=system_prompt
        )
        
        return answer
        
    except Exception as e:
        logger.error(f"Error in RAG answer for merchant {merchant_id}: {e}")
        return f"Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Error: {str(e)}"


async def get_merchant_context(merchant_id: str, limit: int = 10) -> str:
    """
    Get general context about a merchant's business from embeddings
    Used to build dynamic system prompts
    """
    try:
        # Try to get diverse samples from different object types
        context_parts = []
        
        for obj_type in ["product", "faq", "transaction_summary", "risk_assessment"]:
            results = search_vectors(
                merchant_id=merchant_id,
                query_vector=[0.0] * 1536,  # Dummy vector to get random samples
                limit=3,
                object_type=obj_type
            )
            
            for result in results:
                payload = result.get("payload", {})
                text = payload.get("text", "")
                if text:
                    context_parts.append(f"- {text[:200]}")  # First 200 chars
        
        if not context_parts:
            return "No merchant data available yet."
        
        return "\n".join(context_parts[:limit])
        
    except Exception as e:
        logger.error(f"Error getting merchant context: {e}")
        return "Unable to retrieve merchant context."

