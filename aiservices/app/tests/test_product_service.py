"""
Tests for product service
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services import product_service

# Setup test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_create_product(db):
    """Test creating a product"""
    product_data = ProductCreate(
        merchant_id="test_merchant",
        name="Test Product",
        description="A test product description",
        stock=100,
        price=10000,
        ingredients="tepung, gula",
        category="test"
    )
    
    product = await product_service.create_product(db, product_data)
    
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.merchant_id == "test_merchant"
    assert product.stock == 100


def test_get_product(db):
    """Test getting a product"""
    # Create a product first
    product = Product(
        merchant_id="test_merchant",
        name="Test Product",
        stock=50,
        price=5000
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Get the product
    retrieved = product_service.get_product(db, product.id)
    
    assert retrieved is not None
    assert retrieved.id == product.id
    assert retrieved.name == "Test Product"


@pytest.mark.asyncio
async def test_update_product(db):
    """Test updating a product"""
    # Create a product
    product = Product(
        merchant_id="test_merchant",
        name="Old Name",
        stock=10,
        price=1000
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Update the product
    update_data = ProductUpdate(name="New Name", stock=20)
    updated = await product_service.update_product(db, product.id, update_data)
    
    assert updated.name == "New Name"
    assert updated.stock == 20
    assert updated.price == 1000  # Unchanged


def test_delete_product(db):
    """Test deleting a product"""
    # Create a product
    product = Product(
        merchant_id="test_merchant",
        name="To Delete",
        stock=5,
        price=500
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    product_id = product.id
    
    # Delete the product
    success = product_service.delete_product(db, product_id)
    
    assert success is True
    assert product_service.get_product(db, product_id) is None


def test_get_products_by_ingredient(db):
    """Test finding products by ingredient"""
    # Create products with different ingredients
    product1 = Product(
        merchant_id="test_merchant",
        name="Roti",
        ingredients="tepung, gula",
        stock=10,
        price=5000
    )
    product2 = Product(
        merchant_id="test_merchant",
        name="Kopi",
        ingredients="kopi arabica, gula",
        stock=20,
        price=3000
    )
    product3 = Product(
        merchant_id="test_merchant",
        name="Gorengan",
        ingredients="tepung, minyak",
        stock=30,
        price=1000
    )
    
    db.add_all([product1, product2, product3])
    db.commit()
    
    # Search for products with "tepung"
    results = product_service.get_products_by_ingredient(db, "test_merchant", "tepung")
    
    assert len(results) == 2
    names = [p.name for p in results]
    assert "Roti" in names
    assert "Gorengan" in names
    assert "Kopi" not in names
