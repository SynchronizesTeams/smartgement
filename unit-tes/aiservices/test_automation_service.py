"""Unit tests for automation service"""
import pytest
from app.services import automation_service
from app.models.product import Product


@pytest.mark.asyncio
async def test_preview_automation_empty_stock(test_db, multiple_products, test_merchant_id, mock_llm_client):
    """Test preview automation for emptying stock"""
    command = "Kosongkan semua produk yang mengandung tepung"
    
    preview = await automation_service.preview_automation(test_db, test_merchant_id, command)
    
    assert preview["success"] == True
    assert preview["operation_type"] == "empty_stock"
    assert preview["affected_count"] >= 2  # Should find products with tepung
    assert "tepung" in preview["description"].lower()


@pytest.mark.asyncio
async def test_preview_automation_no_products_found(test_db, test_merchant_id, mock_llm_client):
    """Test preview automation when no products match"""
    command = "Hapus semua produk xyz123"
    
    preview = await automation_service.preview_automation(test_db, test_merchant_id, command)
    
    assert preview["success"] == False
    assert "tidak ada produk" in preview["error"].lower()


@pytest.mark.asyncio
async def test_find_affected_products_by_search_query(test_db, multiple_products, test_merchant_id):
    """Test finding products by search query"""
    filters = {
        "search_query": "roti",
        "description": "roti products"
    }
    
    products = await automation_service._find_affected_products(test_db, test_merchant_id, filters)
    
    assert len(products) == 2  # Roti Tawar and Roti Isi Daging
    product_names = [p.name for p in products]
    assert "Roti Tawar" in product_names
    assert "Roti Isi Daging" in product_names


@pytest.mark.asyncio
async def test_find_affected_products_by_ingredient(test_db, multiple_products, test_merchant_id):
    """Test finding products by ingredient"""
    filters = {
        "ingredient": "tepung",
        "description": "products with flour"
    }
    
    products = await automation_service._find_affected_products(test_db, test_merchant_id, filters)
    
    assert len(products) >= 2  # Should find products containing tepung
    for product in products:
        assert "tepung" in product.ingredients.lower()


@pytest.mark.asyncio
async def test_execute_automation_empty_stock(test_db, multiple_products, test_merchant_id, mock_llm_client):
    """Test executing automation to empty stock"""
    command = "Kosongkan stok roti tawar"
    
    result = await automation_service.execute_automation(
        test_db, test_merchant_id, command, confirmed=True
    )
    
    assert result["success"] == True
    assert result["affected_count"] >= 1
    
    # Verify stock is actually set to 0
    product = test_db.query(Product).filter(Product.name == "Roti Tawar").first()
    assert product.stock == 0


@pytest.mark.asyncio
async def test_execute_automation_requires_confirmation(test_db, multiple_products, test_merchant_id, mock_llm_client):
    """Test that high-impact operations require confirmation"""
    # Create many products to trigger confirmation requirement
    for i in range(10):
        from conftest import create_test_product
        create_test_product(test_db, test_merchant_id, name=f"Product {i}", ingredients="tepung")
    
    command = "Kosongkan semua produk yang mengandung tepung"
    
    result = await automation_service.execute_automation(
        test_db, test_merchant_id, command, confirmed=False
    )
    
    assert result["success"] == False
    assert result["requires_confirmation"] == True


@pytest.mark.asyncio
async def test_parse_automation_command(test_merchant_id, mock_llm_client):
    """Test parsing automation command with LLM"""
    command = "Hapus semua roti isi daging"
    
    parsed = await automation_service._parse_automation_command(command, test_merchant_id)
    
    assert parsed["success"] == True
    assert "action" in parsed
    assert "filters" in parsed


@pytest.mark.asyncio
async def test_undo_last_operation(test_db, sample_product, test_merchant_id):
    """Test undo functionality"""
    from app.models.product import AutomationHistory
    
    # Create automation history
    history = AutomationHistory(
        merchant_id=int(test_merchant_id),
        operation_type="empty_stock",
        command="Test command",
        affected_product_ids=[sample_product.id],
        previous_state={
            str(sample_product.id): {
                "stock": 50,
                "name": sample_product.name,
                "price": sample_product.price
            }
        }
    )
    test_db.add(history)
    test_db.commit()
    
    # Change the stock
    sample_product.stock = 0
    test_db.commit()
    
    # Undo
    result = await automation_service.undo_last_operation(test_db, test_merchant_id)
    
    assert result["success"] == True
    assert result["restored_count"] >= 1
    
    # Verify stock is restored
    test_db.refresh(sample_product)
    assert sample_product.stock == 50


@pytest.mark.asyncio
async def test_get_automation_history(test_db, test_merchant_id):
    """Test retrieving automation history"""
    from app.models.product import AutomationHistory
    
    # Create some history records
    for i in range(3):
        history = AutomationHistory(
            merchant_id=int(test_merchant_id),
            operation_type="empty_stock",
            command=f"Test command {i}",
            affected_product_ids=[1, 2, 3],
            previous_state={}
        )
        test_db.add(history)
    test_db.commit()
    
    history_list = automation_service.get_automation_history(test_db, test_merchant_id, limit=10)
    
    assert len(history_list) == 3
    assert all("operation_type" in h for h in history_list)
    assert all("command" in h for h in history_list)
