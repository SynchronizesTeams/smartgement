from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.qdrant_setup import client, create_collection_if_not_exists
from app.services.llm_client import get_embedding

async def create_product(db: Session, product: ProductCreate) -> Product:
    """Create a new product and index it in Qdrant"""
    # Create product in database
    db_product = Product(
        merchant_id=product.merchant_id,
        name=product.name,
        description=product.description,
        stock=product.stock,
        price=product.price,
        ingredients=product.ingredients,
        expiration_date=product.expiration_date,
        category=product.category
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Create embedding and store in Qdrant
    if product.description or product.ingredients:
        collection_name = f"merchant_{product.merchant_id}"
        create_collection_if_not_exists(collection_name)

        # Build embedding text
        text_to_embed = (
            f"{product.name}. "
            f"{product.description or ''}. "
            f"Ingredients: {product.ingredients or ''}"
        )

        embedding = await get_embedding(text_to_embed)

        object_id = f"prod-{db_product.id}"

        payload = {
            "merchant_id": product.merchant_id,
            "object_type": "product",
            "object_id": object_id,
            "text": text_to_embed,
            "name": product.name,
            "description": product.description,
            "ingredients": product.ingredients,
            "category": product.category
        }

        client.upsert(
            collection_name=collection_name,
            points=[{
                "id": object_id,  # IMPORTANT: keep ID as string
                "vector": embedding,
                "payload": payload
            }]
        )

    return db_product


def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Get a single product by ID"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(
    db: Session, 
    merchant_id: str, 
    skip: int = 0, 
    limit: int = 100,
    category: Optional[str] = None
) -> List[Product]:
    """Get all products for a merchant"""
    query = db.query(Product).filter(Product.merchant_id == merchant_id)
    
    if category:
        query = query.filter(Product.category == category)
    
    return query.offset(skip).limit(limit).all()


async def update_product(
    db: Session, 
    product_id: int, 
    product_update: ProductUpdate
) -> Optional[Product]:
    """Update a product"""
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    # Update fields
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db_product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_product)
    
    # Update Qdrant embedding if description changed
    if product_update.description is not None or product_update.ingredients is not None:
        collection_name = f"merchant_{db_product.merchant_id}"
        text_to_embed = f"{db_product.name}. {db_product.description or ''}. Ingredients: {db_product.ingredients or ''}"
        embedding = await get_embedding(text_to_embed)
        
        client.upsert(
            collection_name=collection_name,
            points=[{
                "id": db_product.id,
                "vector": embedding,
                "payload": {
                    "product_id": db_product.id,
                    "merchant_id": db_product.merchant_id,
                    "name": db_product.name,
                    "description": db_product.description,
                    "ingredients": db_product.ingredients,
                    "category": db_product.category
                }
            }]
        )
    
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """Delete a product"""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    merchant_id = db_product.merchant_id
    
    # Delete from database
    db.delete(db_product)
    db.commit()
    
    # Delete from Qdrant
    try:
        collection_name = f"merchant_{merchant_id}"
        client.delete(
            collection_name=collection_name,
            points_selector=[product_id]
        )
    except Exception:
        pass  # Collection might not exist
    
    return True


async def search_products_semantic(
    merchant_id: str,
    query: str,
    limit: int = 10
) -> List[dict]:
    """Semantic search for products using Qdrant"""
    collection_name = f"merchant_{merchant_id}"
    
    try:
        # Generate query embedding
        query_embedding = await get_embedding(query)
        
        # Search in Qdrant
        results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        return [
            {
                "product_id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]
    except Exception as e:
        # Collection might not exist yet
        return []


def get_products_by_ingredient(
    db: Session,
    merchant_id: str,
    ingredient: str
) -> List[Product]:
    """Find products containing a specific ingredient"""
    return db.query(Product).filter(
        Product.merchant_id == merchant_id,
        Product.ingredients.ilike(f"%{ingredient}%")
    ).all()
