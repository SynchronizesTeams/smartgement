"""Unit tests for product service"""
import pytest
from app.services import product_service
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product


@pytest.mark.asyncio
async def test_create_product(test_db, test_merchant_id):
    """Test creating a new product"""
    product_data = ProductCreate(
        merchant_id=test_merchant_id,  # Use string
        name="Test Product",
        price=10000.0,
        stock=20,
        description="Test description",
        category="Test Category"
    )
    
    product = await product_service.create_product(test_db, product_data)
    
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.price == 10000.0
    assert product.stock == 20
    assert product.merchant_id == int(test_merchant_id)


def test_get_products(test_db, multiple_products, test_merchant_id):
    """Test retrieving products for a merchant"""
    products = product_service.get_products(test_db, test_merchant_id)
    
    assert len(products) == len(multiple_products)
    product_names = [p.name for p in products]
    assert "Roti Tawar" in product_names
    assert "Kopi Hitam" in product_names


def test_get_product_by_id(test_db, sample_product, test_merchant_id):
    """Test getting a specific product by ID"""
    product = product_service.get_product_by_id(test_db, sample_product.id, int(test_merchant_id))
    
    assert product is not None
    assert product.id == sample_product.id
    assert product.name == sample_product.name


def test_get_product_by_id_wrong_merchant(test_db, sample_product):
    """Test that products are isolated by merchant"""
    product = product_service.get_product_by_id(test_db, sample_product.id, merchant_id=999)
    
    assert product is None


@pytest.mark.asyncio
async def test_update_product(test_db, sample_product):
    """Test updating a product"""
    update_data = ProductUpdate(
        price=20000.0,
        stock=100
    )
    
    updated = await product_service.update_product(test_db, sample_product.id, update_data)
    
    assert updated.price == 20000.0
    assert updated.stock == 100
    assert updated.name == sample_product.name  # Unchanged field


def test_delete_product(test_db, sample_product):
    """Test deleting a product"""
    product_id = sample_product.id
    
    result = product_service.delete_product(test_db, product_id)
    
    assert result == True
    
    # Verify deletion
    product = test_db.query(Product).filter(Product.id == product_id).first()
    assert product is None


def test_get_products_by_ingredient(test_db, multiple_products, test_merchant_id):
    """Test finding products by ingredient"""
    products = product_service.get_products_by_ingredient(
        test_db, test_merchant_id, "tepung"
    )
    
    assert len(products) >= 2  # Should find products with tepung
    for product in products:
        assert "tepung" in product.ingredients.lower()


def test_get_products_pagination(test_db, test_merchant_id):
    """Test product pagination"""
    # Create many products
    for i in range(15):
        from conftest import create_test_product
        create_test_product(test_db, test_merchant_id, name=f"Product {i}")
    
    # Test limit
    products_limited = product_service.get_products(test_db, test_merchant_id, limit=5)
    assert len(products_limited) == 5
    
    # Test offset
    products_offset = product_service.get_products(test_db, test_merchant_id, skip=5, limit=5)
    assert len(products_offset) == 5
    assert products_offset[0].id != products_limited[0].id
