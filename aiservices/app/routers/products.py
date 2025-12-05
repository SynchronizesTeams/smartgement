from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    SemanticSearchRequest, SemanticSearchResponse
)
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.services import product_service

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    return await product_service.create_product(db, product)


@router.get("/", response_model=List[ProductResponse])
def get_products(
    merchant_id: str,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products for a merchant"""
    return product_service.get_products(db, merchant_id, skip, limit, category)



@router.get("/qdrant", response_model=dict)
async def get_products_from_qdrant(
    merchant_id: str,
    skip: int = 0,
    limit: int = 10
):
    """
    Get products directly from Qdrant for a specific merchant.
    Returns the raw payload from the vector database.
    """
    from app.services.qdrant_setup import client
    
    collection = f"merchant_{merchant_id}"

    # tambahkan filter object_type=product
    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="merchant_id",
                match=MatchValue(value=merchant_id)
            ),
            FieldCondition(
                key="object_type",
                match=MatchValue(value="product")
            )
        ]
    )

    try:
        # gunakan scroll untuk pagination data list
        points, next_page = client.scroll(
            collection_name=collection,
            scroll_filter=qdrant_filter,
            limit=limit,
            offset=skip,
            with_payload=True,
            with_vectors=False
        )

        # hanya ambil payload JSON
        results = [p.payload for p in points]

        return {
            "data": results,
            "next_offset": next_page
        }
    except Exception as e:
        # Handle case where collection might not exist
        return {
            "data": [],
            "next_offset": None,
            "message": str(e)
        }


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    product = await product_service.update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None


@router.post("/search", response_model=SemanticSearchResponse)
async def semantic_search(
    request: SemanticSearchRequest,
    db: Session = Depends(get_db)
):
    """Semantic search for products"""
    results = await product_service.search_products_semantic(
        request.merchant_id,
        request.query,
        request.limit
    )
    
    # Get full product details
    product_ids = [r["product_id"] for r in results]
    products = db.query(product_service.Product).filter(
        product_service.Product.id.in_(product_ids)
    ).all()
    
    # Maintain order and scores from search results
    product_map = {p.id: p for p in products}
    ordered_products = []
    scores = []
    
    for result in results:
        pid = result["product_id"]
        if pid in product_map:
            ordered_products.append(product_map[pid])
            scores.append(result["score"])
    
    return SemanticSearchResponse(
        query=request.query,
        results=[ProductResponse.model_validate(p) for p in ordered_products],
        scores=scores
    )


@router.get("/by-ingredient/{ingredient}", response_model=List[ProductResponse])
def get_by_ingredient(
    ingredient: str,
    merchant_id: str,
    db: Session = Depends(get_db)
):
    """Find products containing a specific ingredient"""
    products = product_service.get_products_by_ingredient(db, merchant_id, ingredient)
    return [ProductResponse.model_validate(p) for p in products]
