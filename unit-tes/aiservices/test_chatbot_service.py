"""Unit tests for chatbot service"""
import pytest
from app.services import chatbot_service
from app.schemas.product import ChatMessage
from app.models.product import Product


@pytest.mark.asyncio
async def test_classify_intent_add_product(mock_llm_global, monkeypatch):
    """Test intent classification for adding product"""
    message = "Tambahkan produk Roti Tawar harga 15000"
    
    # Override mock to return add_product intent
    async def mock_add(prompt, system_prompt=None):
        return '{"intent": "add_product", "confidence": 0.95}'
    
    import app.services.llm_client as llm
    monkeypatch.setattr(llm, "generate_text", mock_add)
    
    result = await chatbot_service.classify_intent(message)
    
    assert result["intent"] == "add_product"
    assert result["confidence"] >= 0.8


@pytest.mark.asyncio
async def test_classify_intent_automation(mock_llm_global, monkeypatch):
    """Test intent classification for automation"""
    message = "Kosongkan semua produk yang mengandung tepung"
    
    async def mock_automation(prompt, system_prompt=None):
        return '{"intent": "automation", "confidence": 0.95}'
    
    import app.services.llm_client as llm
    monkeypatch.setattr(llm, "generate_text", mock_automation)
    
    result = await chatbot_service.classify_intent(message)
    
    assert result["intent"] == "automation"


@pytest.mark.asyncio
async def test_handle_list_products(test_db, multiple_products, test_merchant_id):
    """Test listing products via chatbot"""
    response, actions = await chatbot_service._handle_list_products(test_db, test_merchant_id)
    
    assert "Daftar Produk" in response
    assert str(len(multiple_products)) in response
    assert "Roti Tawar" in response
    assert "Kopi Hitam" in response
    assert len(actions) > 0


@pytest.mark.asyncio
async def test_handle_list_products_empty(test_db, test_merchant_id):
    """Test listing products when none exist"""
    response, actions = await chatbot_service._handle_list_products(test_db, test_merchant_id)
    
    assert "belum memiliki produk" in response.lower()


@pytest.mark.asyncio
async def test_handle_add_product(test_db, test_merchant_id, mock_llm_global, monkeypatch):
    """Test adding product via chatbot"""
    message = "Tambahkan produk Kopi Susu harga 20000 stok 30"
    
    # Mock LLM to extract product details
    async def mock_extract(prompt, system_prompt=None):
        return '{"name": "Kopi Susu", "price": 20000, "stock": 30}'
    
    import app.services.llm_client as llm
    monkeypatch.setattr(llm, "generate_text", mock_extract)
    
    response, actions = await chatbot_service._handle_add_product(test_db, test_merchant_id, message)
    
    assert "berhasil ditambahkan" in response.lower()
    assert "Kopi Susu" in response
    
    # Verify product was created
    product = test_db.query(Product).filter(Product.name == "Kopi Susu").first()
    assert product is not None
    assert product.price == 20000.0
    assert product.stock == 30


@pytest.mark.asyncio
async def test_handle_edit_product(test_db, sample_product, test_merchant_id, mock_llm_global, monkeypatch):
    """Test editing product via chatbot"""
    message = "Ubah harga Roti Tawar jadi 12000"
    
    # Mock LLM to extract edit details
    async def mock_extract(prompt, system_prompt=None):
        return '{"search_query": "Roti Tawar", "updates": {"price": 12000}}'
    
    import app.services.llm_client as llm
    monkeypatch.setattr(llm, "generate_text", mock_extract)
    
    response, actions = await chatbot_service._handle_edit_product(test_db, test_merchant_id, message)
    
    assert "berhasil diupdate" in response.lower()
    
    # Verify price was updated
    test_db.refresh(sample_product)
    assert sample_product.price == 12000.0


@pytest.mark.asyncio
async def test_handle_delete_product(test_db, sample_product, test_merchant_id, mock_llm_global, monkeypatch):
    """Test deleting product via chatbot"""
    message = "Hapus produk Roti Tawar"
    
    # Mock LLM to extract product name
    async def mock_extract(prompt, system_prompt=None):
        return '{"search_query": "Roti Tawar"}'
    
    import app.services.llm_client as llm
    monkeypatch.setattr(llm, "generate_text", mock_extract)
    
    response, actions = await chatbot_service._handle_delete_product(test_db, test_merchant_id, message)
    
    assert "berhasil dihapus" in response.lower()
    assert "Roti Tawar" in response
    
    # Verify product was deleted
    product = test_db.query(Product).filter(Product.name == "Roti Tawar").first()
    assert product is None


@pytest.mark.asyncio
async def test_handle_query(test_db, multiple_products, test_merchant_id, mock_llm_global):
    """Test query handling with product context"""
    message = "Berapa stok kopi?"
    
    response, actions = await chatbot_service._handle_query(
        test_db, test_merchant_id, message, ""
    )
    
    assert isinstance(response, str)
    assert len(actions) > 0


@pytest.mark.asyncio
async def test_is_list_request():
    """Test list request detection"""
    assert chatbot_service._is_list_request("Tampilkan semua produk")
    assert chatbot_service._is_list_request("Daftar barang saya")
    assert chatbot_service._is_list_request("Lihat semua item")
    assert not chatbot_service._is_list_request("Hapus produk")
    assert not chatbot_service._is_list_request("Tambah kopi")


@pytest.mark.asyncio
async def test_process_chat_message(test_db, test_merchant_id, mock_llm_global):
    """Test full chat message processing flow"""
    message = ChatMessage(
        merchant_id=test_merchant_id,
        message="Tampilkan semua produk",
        conversation_history=[]
    )
    
    response = await chatbot_service.process_chat_message(test_db, message)
    
    assert response.response is not None
    assert response.intent is not None
    assert 0 <= response.confidence <= 1
    assert isinstance(response.suggested_actions, list)
