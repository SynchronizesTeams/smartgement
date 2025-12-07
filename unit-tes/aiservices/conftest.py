"""Pytest configuration and fixtures for AI services tests"""
import pytest
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock, MagicMock

# Add aiservices to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "aiservices"))

from app.database import Base
from app.models.product import Product, ChatHistory, AutomationHistory


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def test_merchant_id():
    """Return a test merchant ID"""
    return "1"


@pytest.fixture
def sample_product(test_db, test_merchant_id):
    """Create a sample product for testing"""
    product = Product(
        merchant_id=int(test_merchant_id),
        name="Roti Tawar",
        price=15000.0,
        stock=50,
        description="Roti tawar segar",
        category="Bakery",
        ingredients="tepung, ragi, gula"
    )
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)
    return product


@pytest.fixture
def multiple_products(test_db, test_merchant_id):
    """Create multiple products for testing"""
    products = [
        Product(
            merchant_id=int(test_merchant_id),
            name="Roti Tawar",
            price=15000.0,
            stock=50,
            ingredients="tepung"
        ),
        Product(
            merchant_id=int(test_merchant_id),
            name="Kopi Hitam",
            price=25000.0,
            stock=100,
            ingredients="kopi"
        ),
        Product(
            merchant_id=int(test_merchant_id),
            name="Roti Isi Daging",
            price=20000.0,
            stock=30,
            ingredients="tepung, daging"
        ),
    ]
    for product in products:
        test_db.add(product)
    test_db.commit()
    return products


@pytest.fixture
def mock_llm_client(monkeypatch):
    """Mock the LLM client to avoid API calls"""
    async def mock_generate_text(prompt, system_prompt=None):
        # Return different responses based on the prompt content
        if "intent" in prompt.lower() or "classify" in prompt.lower():
            return '{"intent": "query", "confidence": 0.8}'
        elif "automation" in prompt.lower() or "parse" in prompt.lower():
            return '{"action": "empty_stock", "filters": {"search_query": "tepung", "ingredient": "tepung", "description": "produk yang mengandung tepung"}}'
        elif "extract product" in prompt.lower():
            return '{"name": "Roti Tawar", "price": 15000, "stock": 50}'
        elif "extract edit" in prompt.lower():
            return '{"search_query": "Roti Tawar", "updates": {"price": 12000}}'
        elif "extract product name to delete" in prompt.lower():
            return '{"search_query": "Roti Tawar"}'
        else:
            return "Berikut adalah informasi yang Anda minta."
    
    # Patch the generate_text function
    from app.services import llm_client
    monkeypatch.setattr(llm_client, "generate_text", mock_generate_text)
    return mock_generate_text


@pytest.fixture
def mock_qdrant_client(monkeypatch):
    """Mock Qdrant client to avoid external service calls"""
    mock_client = MagicMock()
    return mock_client


# Helper functions for test data
def create_test_product(db, merchant_id, **kwargs):
    """Helper to create a test product with default values"""
    defaults = {
        "merchant_id": int(merchant_id),
        "name": "Test Product",
        "price": 10000.0,
        "stock": 10,
        "description": "Test description",
        "category": "Test",
    }
    defaults.update(kwargs)
    product = Product(**defaults)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
