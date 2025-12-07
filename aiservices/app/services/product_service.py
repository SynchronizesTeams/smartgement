from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

async def create_product(db: Session, product: ProductCreate) -> Product:
    """Create a new product"""
    db_product = Product(
        merchant_id=int(product.merchant_id),
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
    query = db.query(Product).filter(Product.merchant_id == int(merchant_id))
    
    if category:
        query = query.filter(Product.category == category)
    
    return query.offset(skip).limit(limit).all()


def get_product_by_id(
    db: Session,
    product_id: int,
    merchant_id: int
) -> Optional[Product]:
    """Get a single product by ID for a specific merchant (ensures isolation)"""
    return db.query(Product).filter(
        Product.id == product_id,
        Product.merchant_id == merchant_id
    ).first()


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
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """Delete a product"""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True


def get_products_by_ingredient(
    db: Session,
    merchant_id: str,
    ingredient: str
) -> List[Product]:
    """Get products by ingredient"""
    return db.query(Product).filter(
        Product.merchant_id == int(merchant_id),
        Product.ingredients.ilike(f"%{ingredient}%")
    ).all()


def search_products_by_name(
    db: Session,
    merchant_id: str,
    name: str
) -> List[Product]:
    """Search products by name"""
    return db.query(Product).filter(
        Product.merchant_id == int(merchant_id),
        Product.name.ilike(f"%{name}%")
    ).all()


def search_products_by_category(
    db: Session,
    merchant_id: str,
    category: str
) -> List[Product]:
    """Search products by category"""
    return db.query(Product).filter(
        Product.merchant_id == int(merchant_id),
        Product.category.ilike(f"%{category}%")
    ).all()
