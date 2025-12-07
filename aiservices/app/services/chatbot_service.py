from sqlalchemy.orm import Session
from typing import Dict
from app.models.product import Product
from app.services.llm_client import generate_text
from app.services.automation_service import preview_automation, execute_automation
from app.services.risk_services import get_high_risk_products, generate_risk_report
from app.schemas.product import ChatMessage, ChatResponse
import json
import logging

logger = logging.getLogger(__name__)


# Hardcoded chatbot prompt - centralized configuration
chatbot_prompt = """You are an AI assistant for a merchant's business management system.
You help with product management, risk analysis, automation, and business insights.

Your capabilities:
1. **Product CRUD**: Add, edit, delete, and list products
2. **Automation**: Help execute bulk operations on products (delete, update stock, etc.)
3. **Risk Analysis**: Identify high-risk products, expiring items, and business health issues
4. **Transaction Analysis**: Summarize sales, analyze revenue trends, and provide transaction insights
5. **Query & Analysis**: Answer questions about products, sales, trends, and inventory
6. **Recommendations**: Provide actionable insights based on business data

Guidelines:
- Be concise and actionable
- Respond in Indonesian (Bahasa Indonesia) for a friendly tone
- Provide specific product names and data when relevant
- If you don't have enough information, ask clarifying questions
- Focus on helping merchants make better business decisions

Examples of what you can do:
- "Tambahkan produk Roti Tawar harga 15000" (Add Product)
- "Ubah harga Roti Tawar jadi 12000" (Edit Product)
- "Hapus produk Roti Tawar" (Delete Product)
- "Tampilkan semua produk" (List Products)
- "Kosongkan semua produk yang mengandung tepung" (Automation)
- "Produk apa yang berisiko tinggi?" (Risk Analysis)
- "Berapa penjualan roti minggu ini?" (Query)
- "Ringkas transaksi hari ini" (Transaction Summary)
"""


async def process_chat_message(
    db: Session,
    message: ChatMessage
) -> ChatResponse:
    """Main entry point for processing chat messages"""
    from app.models.product import ChatHistory
    
    # Use hardcoded chatbot prompt
    system_prompt = chatbot_prompt
    
    # Build conversation context if history is provided
    conversation_context = ""
    if message.conversation_history and len(message.conversation_history) > 0:
        conversation_context = "\n\nPrevious conversation:\n"
        for msg in message.conversation_history:
            role = "User" if msg.get("role") == "user" else "Assistant"
            conversation_context += f"{role}: {msg.get('content', '')}\n"
        conversation_context += f"\nCurrent message from User: {message.message}\n"
    else:
        conversation_context = f"\nUser: {message.message}\n"
    
    # Classify intent with conversation context
    intent_result = await classify_intent(message.message, system_prompt, conversation_context)
    intent = intent_result["intent"]
    confidence = intent_result["confidence"]
    
    # Route to appropriate handler (pass conversation context for query handler)
    if intent == "automation":
        response_text, suggested_actions = await _handle_automation_request(
            db, message.merchant_id, message.message
        )
    elif intent == "add_product":
        response_text, suggested_actions = await _handle_add_product(
            db, message.merchant_id, message.message
        )
    elif intent == "edit_product":
        response_text, suggested_actions = await _handle_edit_product(
            db, message.merchant_id, message.message
        )
    elif intent == "delete_product":
        response_text, suggested_actions = await _handle_delete_product(
            db, message.merchant_id, message.message
        )
    elif _is_list_request(message.message):
         response_text, suggested_actions = await _handle_list_products(
            db, message.merchant_id
        )
    elif intent == "risk_report":
        response_text, suggested_actions = await _handle_risk_report(db, message.merchant_id)
    elif intent == "transaction_summary":
        response_text, suggested_actions = await _handle_transaction_summary(
            db, message.merchant_id, message.message
        )
    elif intent == "query":
        # Pass conversation context to query handler
        response_text, suggested_actions = await _handle_query(
            db, message.merchant_id, message.message, conversation_context
        )
    else:
        response_text, suggested_actions = await _handle_help(message.message)
    
    # Save chat history
    try:
        chat_record = ChatHistory(
            merchant_id=message.merchant_id,
            user_message=message.message,
            ai_response=response_text,
            intent=intent
        )
        db.add(chat_record)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to save chat history: {e}")
        db.rollback()
    
    return ChatResponse(
        response=response_text,
        intent=intent,
        confidence=confidence,
        suggested_actions=suggested_actions
    )


async def classify_intent(message: str, system_prompt: str = None, conversation_context: str = "") -> Dict:
    """Classify user intent from message"""
    prompt = f"""
Classify the following message into one of these intents:
- "add_product": User wants to add/create a new product
- "edit_product": User wants to edit/update an existing product
- "delete_product": User wants to delete/remove a product
- "automation": User wants to perform bulk operations (delete many, update stock for many, etc.)
- "risk_report": User asks about risks, expiring products, or problems
- "transaction_summary": User asks for transaction summaries, sales analysis, or revenue insights
- "query": User asks questions about products, trends, or analytics
- "help": General help or unclear request

{conversation_context}

Return JSON with:
- intent: one of the above
- confidence: 0.0 to 1.0

Examples:
"Tambahkan produk Roti Tawar harga 15000" -> {{"intent": "add_product", "confidence": 0.95}}
"Ubah harga Roti Tawar jadi 12000" -> {{"intent": "edit_product", "confidence": 0.9}}
"Hapus produk Roti Tawar" -> {{"intent": "delete_product", "confidence": 0.95}}
"Kosongkan semua produk yang mengandung tepung" -> {{"intent": "automation", "confidence": 0.95}}
"Produk apa yang berisiko tinggi?" -> {{"intent": "risk_report", "confidence": 0.9}}
"Ringkas transaksi hari ini" -> {{"intent": "transaction_summary", "confidence": 0.95}}
"Berapa total penjualan minggu ini?" -> {{"intent": "transaction_summary", "confidence": 0.9}}
"Berapa penjualan roti minggu ini?" -> {{"intent": "query", "confidence": 0.85}}

Only return JSON, nothing else.
"""
    
    try:
        response = await generate_text(prompt, system_prompt=system_prompt)
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(response)
        return result
    except Exception:
        return {"intent": "query", "confidence": 0.5}


async def _handle_automation_request(
    db: Session,
    merchant_id: str,
    message: str
) -> tuple[str, list[str]]:
    """Handle automation requests"""
    # Get preview
    preview = await preview_automation(db, merchant_id, message)
    
    if not preview["success"]:
        return (
            f"Maaf, saya tidak bisa memahami perintah automasi tersebut. {preview.get('error', '')}",
            ["Coba ulangi dengan lebih spesifik", "Minta bantuan"]
        )
    
    # Return preview with confirmation prompt
    product_names = [p.name for p in preview["affected_products"][:5]]
    more_count = max(0, preview["affected_count"] - 5)
    
    product_list = "\n- ".join(product_names)
    if more_count > 0:
        product_list += f"\n... dan {more_count} produk lainnya"
    
    response = f"""
📋 **Preview Automasi**

**Operasi**: {preview['description']}
**Produk yang terpengaruh**: {preview['affected_count']} produk

**Produk yang akan diubah**:
- {product_list}

⚠️ **Dampak**: {preview['estimated_impact']}

{"❗ Konfirmasi diperlukan untuk operasi ini." if preview['requires_confirmation'] else ""}
"""
    
    suggested_actions = [
        "Eksekusi operasi ini",
        "Batal",
        "Lihat detail produk"
    ]
    
    return (response, suggested_actions)


async def _handle_risk_report(db: Session, merchant_id: str) -> tuple[str, list[str]]:
    """Handle risk report requests"""
    report = generate_risk_report(db, merchant_id)
    
    response = f"""
🚨 **Laporan Risiko Produk**

**Total Produk**: {report['total_products']}

**Breakdown Risiko**:
- 🔴 Critical: {report['risk_breakdown']['critical']} produk
- 🟠 High: {report['risk_breakdown']['high']} produk
- 🟡 Medium: {report['risk_breakdown']['medium']} produk
- 🟢 Low: {report['risk_breakdown']['low']} produk

"""
    
    if report['top_risks']:
        response += "\n**Top 5 Produk Berisiko Tinggi**:\n"
        for risk in report['top_risks'][:5]:
            response += f"- {risk['product_name']} ({risk['risk_level']}, score: {risk['risk_score']:.0f})\n"
    
    suggested_actions = [
        "Lihat detail produk berisiko",
        "Buat rencana tindakan",
        "Export laporan"
    ]
    
    return (response, suggested_actions)


async def _handle_transaction_summary(
    db: Session,
    merchant_id: str,
    message: str
) -> tuple[str, list[str]]:
    """Handle transaction summary requests"""
    from app.services import transaction_summary_service
    
    try:
        # Analyze query to get summary
        result = await transaction_summary_service.analyze_transaction_query(
            db, merchant_id, message
        )
        
        # Format response
        response = f"""
📊 **Ringkasan Transaksi**

{result['summary']}

**Statistik**:
- Total Transaksi: {result['total_transactions']}
- Total Pendapatan: Rp{result['total_revenue']:,.2f}
- Rata-rata Transaksi: Rp{result['average_transaction']:,.2f}
- Periode: {result['period']}
"""
        
        if result['insights']:
            response += "\n**Insights**:\n"
            for insight in result['insights']:
                response += f"- {insight['title']}: {insight['description']}\n"
        
        suggested_actions = [
            "Lihat detail transaksi",
            "Analisis lebih lanjut",
            "Export laporan"
        ]
        
        return (response, suggested_actions)
        
    except Exception as e:
        logger.error(f"Transaction summary error: {e}")
        return (
            f"Maaf, gagal mengambil ringkasan transaksi. Error: {str(e)}",
            ["Coba lagi", "Bantuan"]
        )


async def _handle_query(
    db: Session,
    merchant_id: str,
    message: str,
    conversation_context: str = ""
) -> tuple[str, list[str]]:
    """Handle general queries using LLM with product data from database"""
    try:
        # Get recent products from database
        from app.services.product_service import get_products
        products = get_products(db, merchant_id, limit=20)
        
        # Build context from database products
        product_context = ""
        if products:
            product_context = "Available products:\n"
            for p in products:
                product_context += f"- {p.name}: Rp {p.price:,.0f}, Stock: {p.stock}"
                if p.description:
                    product_context += f", {p.description}"
                product_context += "\n"
        else:
            product_context = "No products in database yet.\n"
        
        # Build full prompt with context
        full_prompt = f"""{conversation_context}

{product_context}

Based on the conversation and product data above, answer this question: {message}

Answer in Indonesian (Bahasa Indonesia) and be concise and helpful."""
        
        answer = await generate_text(full_prompt, system_prompt=chatbot_prompt)
        suggested_actions = [
            "Analisis tren produk",
            "Cek risiko",
            "Lihat rekomendasi"
        ]
        return (answer, suggested_actions)
    except Exception as e:
        logger.error(f"Query handler error: {e}")
        return (
            f"Maaf, saya mengalami kesulitan menjawab pertanyaan tersebut. Error: {str(e)}",
            ["Coba pertanyaan lain", "Minta bantuan"]
        )


async def _handle_help(message: str) -> tuple[str, list[str]]:
    """Handle help requests"""
    help_text = """
👋 **Asisten Toko AI**

Saya dapat membantu Anda dengan:

1. **Kelola Produk**
   - "Tambahkan produk Roti Tawar harga 15000 stok 50"
   - "Ubah harga Roti Tawar jadi 12000"
   - "Hapus produk Roti Tawar"
   - "Tampilkan semua produk saya"

2. **Automasi** - Kelola produk secara massal
   - "Kosongkan semua produk yang mengandung tepung"
   - "Hapus semua roti yang expired"

3. **Analisis Risiko** - Identifikasi produk bermasalah
   - "Produk apa yang berisiko tinggi?"
   - "Mana yang hampir expired?"

4. **Informasi Produk** - Tanya tentang produk Anda
   - "Berapa penjualan roti minggu ini?"
   - "Produk apa yang paling laris?"

Silakan tanya apa saja!
"""
    
    suggested_actions = [
        "Lihat produk",
        "Tambah produk",
        "Cek risiko"
    ]
    
    return (help_text, suggested_actions)


async def _handle_add_product(
    db: Session,
    merchant_id: str,
    message: str
) -> tuple[str, list[str]]:
    """Handle add product requests"""
    from app.services.product_service import create_product
    from app.schemas.product import ProductCreate
    
    # Use LLM to extract product details
    prompt = f"""
Extract product details from this message: "{message}"

Return JSON with:
- name: product name (required)
- price: product price (required, number)
- stock: initial stock (default 0)
- description: product description
- category: product category
- ingredients: ingredients if mentioned

Example:
"Tambahkan produk Roti Tawar harga 15000 stok 50" -> {{"name": "Roti Tawar", "price": 15000, "stock": 50}}

Only return JSON, nothing else.
"""
    
    try:
        response = await generate_text(prompt)
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        
        product_data = json.loads(response)
        
        # Validate required fields
        if not product_data.get("name") or not product_data.get("price"):
            return (
                "Maaf, saya perlu nama dan harga produk. Contoh: 'Tambahkan produk Roti Tawar harga 15000'",
                ["Coba lagi", "Bantuan"]
            )
        
        # Create product
        product_create = ProductCreate(
            merchant_id=merchant_id,
            name=product_data["name"],
            price=float(product_data["price"]),
            stock=int(product_data.get("stock", 0)),
            description=product_data.get("description"),
            category=product_data.get("category"),
            ingredients=product_data.get("ingredients")
        )
        
        new_product = await create_product(db, product_create)
        
        return (
            f"✅ Produk berhasil ditambahkan!\n\n"
            f"**{new_product.name}**\n"
            f"Harga: Rp {new_product.price:,.0f}\n"
            f"Stok: {new_product.stock}\n"
            f"ID: {new_product.id}",
            ["Lihat semua produk", "Tambah produk lain"]
        )
        
    except Exception as e:
        logger.error(f"Add product error: {e}")
        return (
            f"Maaf, gagal menambahkan produk. Error: {str(e)}",
            ["Coba lagi", "Bantuan"]
        )


async def _handle_edit_product(
    db: Session,
    merchant_id: str,
    message: str
) -> tuple[str, list[str]]:
    """Handle edit product requests"""
    from app.services.product_service import get_products, update_product
    from app.schemas.product import ProductUpdate
    
    # Use LLM to extract product name and updates
    prompt = f"""
Extract edit details from this message: "{message}"

Return JSON with:
- search_query: product name to find
- updates: object with fields to update (price, stock, name, description, etc.)

Example:
"Ubah harga Roti Tawar jadi 12000" -> {{"search_query": "Roti Tawar", "updates": {{"price": 12000}}}}
"Update stok kopi menjadi 100" -> {{"search_query": "kopi", "updates": {{"stock": 100}}}}

Only return JSON, nothing else.
"""
    
    try:
        response = await generate_text(prompt)
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        
        edit_data = json.loads(response)
        search_query = edit_data.get("search_query", "")
        updates = edit_data.get("updates", {})
        
        if not search_query or not updates:
            return (
                "Maaf, saya perlu tahu produk mana yang ingin diubah dan apa yang ingin diubah.",
                ["Coba lagi", "Lihat produk"]
            )
        
        # Find product
        products = db.query(Product).filter(
            Product.merchant_id == int(merchant_id),
            Product.name.ilike(f"%{search_query}%")
        ).all()
        
        if not products:
            return (
                f"Produk '{search_query}' tidak ditemukan.",
                ["Lihat semua produk", "Coba lagi"]
            )
        
        if len(products) > 1:
            product_list = "\n- ".join([p.name for p in products[:5]])
            return (
                f"Ditemukan {len(products)} produk. Spesifikan lebih jelas:\n- {product_list}",
                ["Coba lagi"]
            )
        
        # Update product
        product = products[0]
        product_update = ProductUpdate(**updates)
        updated_product = await update_product(db, product.id, product_update)
        
        return (
            f"✅ Produk berhasil diupdate!\n\n"
            f"**{updated_product.name}**\n"
            f"Harga: Rp {updated_product.price:,.0f}\n"
            f"Stok: {updated_product.stock}",
            ["Lihat produk", "Edit lagi"]
        )
        
    except Exception as e:
        logger.error(f"Edit product error: {e}")
        return (
            f"Maaf, gagal mengupdate produk. Error: {str(e)}",
            ["Coba lagi", "Bantuan"]
        )


async def _handle_delete_product(
    db: Session,
    merchant_id: str,
    message: str
) -> tuple[str, list[str]]:
    """Handle delete product requests"""
    from app.services.product_service import delete_product
    
    # Use LLM to extract product name
    prompt = f"""
Extract product name to delete from: "{message}"

Return JSON with:
- search_query: product name to find and delete

Example:
"Hapus produk Roti Tawar" -> {{"search_query": "Roti Tawar"}}

Only return JSON, nothing else.
"""
    
    try:
        response = await generate_text(prompt)
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        
        delete_data = json.loads(response)
        search_query = delete_data.get("search_query", "")
        
        if not search_query:
            return (
                "Maaf, saya perlu tahu produk mana yang ingin dihapus.",
                ["Lihat produk", "Coba lagi"]
            )
        
        # Find product
        products = db.query(Product).filter(
            Product.merchant_id == int(merchant_id),
            Product.name.ilike(f"%{search_query}%")
        ).all()
        
        if not products:
            return (
                f"Produk '{search_query}' tidak ditemukan.",
                ["Lihat semua produk", "Coba lagi"]
            )
        
        if len(products) > 1:
            product_list = "\n- ".join([p.name for p in products[:5]])
            return (
                f"Ditemukan {len(products)} produk. Spesifikan lebih jelas:\n- {product_list}",
                ["Coba lagi"]
            )
        
        # Delete product
        product = products[0]
        product_name = product.name
        delete_product(db, product.id)
        
        return (
            f"✅ Produk **{product_name}** berhasil dihapus!",
            ["Lihat produk", "Undo"]
        )
        
    except Exception as e:
        logger.error(f"Delete product error: {e}")
        return (
            f"Maaf, gagal menghapus produk. Error: {str(e)}",
            ["Coba lagi", "Bantuan"]
        )


def _is_list_request(message: str) -> bool:
    """Check if message is asking to list products"""
    msg = message.lower()
    keywords = ["list", "daftar", "tampilkan", "lihat", "show", "apa saja", "barang", "produk", "inventory", "stok"]
    
    # Must have "produk"/"barang"/"inventory" AND "list"/"daftar"/"tampilkan"/"lihat"/"show"/"apa"
    has_obj = any(k in msg for k in ["produk", "barang", "item", "inventory", "stok", "etalase"])
    has_act = any(k in msg for k in ["list", "daftar", "tampilkan", "lihat", "show", "cek", "apa"])
    
    return has_obj and has_act


async def _handle_list_products(db: Session, merchant_id: str) -> tuple[str, list[str]]:
    """Handle request to list products - QUERY DATABASE DIRECTLY"""
    from app.services.product_service import get_products
    
    products = get_products(db, merchant_id, limit=50)
    
    if not products:
        return (
            "Anda belum memiliki produk di database.",
            ["Tambah produk baru"]
        )
        
    response = f"📚 **Daftar Produk ({len(products)} item)**:\n\n"
    
    for p in products:
        response += f"- **{p.name}** (Stok: {p.stock}) - Rp {p.price:,.0f}\n"
        if p.description:
            desc = p.description[:50] + "..." if len(p.description) > 50 else p.description
            response += f"  _{desc}_\n"
            
    if len(products) >= 50:
        response += "\n...(menampilkan 50 produk pertama)"
        
    suggested_actions = [
        "Analisis risiko",
        "Tambah produk",
        "Edit produk"
    ]
    
    return (response, suggested_actions)
