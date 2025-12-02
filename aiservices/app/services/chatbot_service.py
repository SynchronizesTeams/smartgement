from sqlalchemy.orm import Session
from typing import Dict
from app.services.llm_client import generate_text
from app.services.rag_services import rag_answer, get_merchant_context
from app.services.automation_service import preview_automation, execute_automation
from app.services.risk_services import get_high_risk_products, generate_risk_report
from app.schemas.product import ChatMessage, ChatResponse
import json
import logging

logger = logging.getLogger(__name__)


async def generate_system_prompt(merchant_id: str) -> str:
    """
    Generate dynamic system prompt based on merchant's embeddings
    This provides context-aware chatbot responses
    """
    try:
        # Get merchant context from embeddings
        context = await get_merchant_context(merchant_id, limit=8)
        
        system_prompt = f"""You are an AI assistant for a merchant's business management system.
You help with product management, risk analysis, automation, and business insights.

Merchant's Business Context:
{context}

Your capabilities:
1. **Automation**: Help execute bulk operations on products
2. **Risk Analysis**: Identify high-risk products, expiring items, and business health issues
3. **Query & Analysis**: Answer questions about products, sales, trends, and inventory
4. **Recommendations**: Provide actionable insights based on business data

Always:
- Be concise and actionable
- Use the merchant's actual data from the context above
- Respond in Indonesian (Bahasa Indonesia) for a friendly tone
- Provide specific product names and data when relevant
- If you don't have enough information, ask clarifying questions
"""
        return system_prompt
    except Exception as e:
        logger.error(f"Error generating system prompt for merchant {merchant_id}: {e}")
        # Return default prompt if context retrieval fails
        return """You are an AI assistant for business management.
Help with product management, risk analysis, and business insights.
Respond in Indonesian (Bahasa Indonesia)."""


async def process_chat_message(
    db: Session,
    message: ChatMessage
) -> ChatResponse:
    """Main entry point for processing chat messages"""
    # Generate dynamic system prompt based on merchant context
    system_prompt = await generate_system_prompt(message.merchant_id)
    
    # Classify intent with merchant context
    intent_result = await classify_intent(message.message, system_prompt)
    intent = intent_result["intent"]
    confidence = intent_result["confidence"]
    
    # Route to appropriate handler
    if intent == "automation":
        response_text, suggested_actions = await _handle_automation_request(
            db, message.merchant_id, message.message
        )
    elif intent == "risk_report":
        response_text, suggested_actions = await _handle_risk_report(db, message.merchant_id)
    elif intent == "query":
        response_text, suggested_actions = await _handle_query(
            db, message.merchant_id, message.message
        )
    else:
        response_text, suggested_actions = await _handle_help(message.message)
    
    return ChatResponse(
        response=response_text,
        intent=intent,
        confidence=confidence,
        suggested_actions=suggested_actions
    )


async def classify_intent(message: str, system_prompt: str = None) -> Dict:
    """Classify user intent from message"""
    prompt = f"""
Classify the following message into one of these intents:
- "automation": User wants to perform bulk operations (delete, update stock, etc.)
- "risk_report": User asks about risks, expiring products, or problems
- "query": User asks questions about products, trends, or analytics
- "help": General help or unclear request

Message: "{message}"

Return JSON with:
- intent: one of the above
- confidence: 0.0 to 1.0

Examples:
"Kosongkan semua produk yang mengandung tepung" -> {{"intent": "automation", "confidence": 0.95}}
"Produk apa yang berisiko tinggi?" -> {{"intent": "risk_report", "confidence": 0.9}}
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


async def _handle_query(
    db: Session,
    merchant_id: str,
    message: str
) -> tuple[str, list[str]]:
    """Handle general queries using RAG"""
    try:
        answer = await rag_answer(merchant_id, message)
        suggested_actions = [
            "Analisis tren produk",
            "Cek risiko",
            "Lihat rekomendasi"
        ]
        return (answer, suggested_actions)
    except Exception as e:
        return (
            f"Maaf, saya mengalami kesulitan menjawab pertanyaan tersebut. Error: {str(e)}",
            ["Coba pertanyaan lain", "Minta bantuan"]
        )


async def _handle_help(message: str) -> tuple[str, list[str]]:
    """Handle help requests"""
    help_text = """
👋 **Asisten Toko AI**

Saya dapat membantu Anda dengan:

1. **Automasi** - Kelola produk secara massal
   - "Kosongkan semua produk yang mengandung tepung"
   - "Hapus semua roti yang expired"

2. **Analisis Risiko** - Identifikasi produk bermasalah
   - "Produk apa yang berisiko tinggi?"
   - "Mana yang hampir expired?"

3. **Informasi Produk** - Tanya tentang produk Anda
   - "Berapa penjualan roti minggu ini?"
   - "Produk apa yang paling laris?"

Silakan tanya apa saja!
"""
    
    suggested_actions = [
        "Lihat produk berisiko",
        "Analisis tren",
        "Automasi stok"
    ]
    
    return (help_text, suggested_actions)
