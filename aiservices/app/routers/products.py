from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse
)
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





@router.get("/by-ingredient/{ingredient}", response_model=List[ProductResponse])
def get_by_ingredient(
    ingredient: str,
    merchant_id: str,
    db: Session = Depends(get_db)
):
    """Find products containing a specific ingredient"""
    products = product_service.get_products_by_ingredient(db, merchant_id, ingredient)
    return [ProductResponse.model_validate(p) for p in products]
