from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime
from app.models.product import Product, AutomationHistory, ChatHistory
from app.services.product_service import get_products_by_ingredient
from app.services.llm_client import generate_text
import json
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

automation_schema = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["empty_stock", "update_stock", "delete", "add_product", "edit_product"]},
        "filters": {
            "type": "object",
            "properties": {
                "search_query": {"type": "string"},
                "ingredient": {"type": "string"},
                "description": {"type": "string"}
            }
        },
        "new_stock": {"type": "number"},
        "product_data": {"type": "object"}
    },
    "required": ["action"]
}


async def preview_automation(
    db: Session,
    merchant_id: str,
    command: str
) -> Dict:
    """Preview what an automation command will do without executing"""
    # Parse the command to understand intent
    parsed = await _parse_automation_command(command, merchant_id)
    
    if not parsed["success"]:
        return {
            "success": False,
            "error": parsed.get("error", "Could not understand command")
        }
    
    action = parsed["action"]
    filters = parsed["filters"]
    
    # Find affected products
    affected_products = await _find_affected_products(db, merchant_id, filters)
    
    # Check if no products found
    if len(affected_products) == 0:
        search_desc = filters.get('description', 'kriteria tersebut')
        return {
            "success": False,
            "error": f"Tidak ada produk yang cocok dengan '{search_desc}'. Coba cek daftar produk Anda atau gunakan kata kunci yang berbeda."
        }
    
    # Generate description
    if action == "empty_stock":
        description = f"Set stock to 0 for all products matching: {filters.get('description', 'unknown criteria')}"
        impact = f"This will mark {len(affected_products)} products as out of stock. Sales will be blocked until restocked."
    elif action == "delete":
        description = f"Delete all products matching: {filters.get('description', 'unknown criteria')}"
        impact = f"This will permanently delete {len(affected_products)} products from your inventory. This cannot be easily undone."
    elif action == "update_stock":
        new_stock = filters.get("new_stock", 0)
        description = f"Update stock to {new_stock} for products matching: {filters.get('description', 'unknown criteria')}"
        impact = f"This will update stock levels for {len(affected_products)} products."
    else:
        description = f"Unknown action: {action}"
        impact = "Cannot determine impact"
    
    return {
        "success": True,
        "operation_type": action,
        "description": description,
        "affected_products": affected_products,
        "affected_count": len(affected_products),
        "estimated_impact": impact,
        "requires_confirmation": len(affected_products) > 5 or action == "delete"
    }


async def execute_automation(
    db: Session,
    merchant_id: str,
    command: str,
    confirmed: bool = False
) -> Dict:
    """Execute an automation command"""
    # Get preview first
    preview = await preview_automation(db, merchant_id, command)
    
    if not preview["success"]:
        return preview
    
    # Check if confirmation required
    if preview["requires_confirmation"] and not confirmed:
        return {
            "success": False,
            "error": "Confirmation required. This operation affects multiple products.",
            "preview": preview,
            "requires_confirmation": True
        }
    
    affected_products = preview["affected_products"]
    action = preview["operation_type"]
    
    # Store previous state for undo
    previous_state = {}
    affected_ids = []
    
    for product in affected_products:
        affected_ids.append(product.id)
        previous_state[product.id] = {
            "stock": product.stock,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }
    
    # Execute action
    try:
        if action == "empty_stock":
            for product in affected_products:
                product.stock = 0
                product.updated_at = datetime.utcnow()
            
        elif action == "update_stock":
            new_stock = await _extract_stock_value(command)
            for product in affected_products:
                product.stock = new_stock
                product.updated_at = datetime.utcnow()
        
        elif action == "delete":
            for product in affected_products:
                db.delete(product)
        
        # Save automation history
        history = AutomationHistory(
            merchant_id=merchant_id,
            operation_type=action,
            command=command,
            affected_product_ids=affected_ids,
            previous_state=previous_state
        )
        db.add(history)
        
        db.commit()
        
        return {
            "success": True,
            "operation_type": action,
            "affected_count": len(affected_products),
            "affected_product_ids": affected_ids,
            "message": f"Successfully executed: {preview['description']}",
            "can_undo": True,
            "operation_id": history.id
        }
    
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Failed to execute automation: {str(e)}"
        }


async def undo_last_operation(
    db: Session,
    merchant_id: str,
    operation_id: Optional[int] = None
) -> Dict:
    """Undo a previous automation operation"""
    if operation_id:
        history = db.query(AutomationHistory).filter(
            AutomationHistory.id == operation_id,
            AutomationHistory.merchant_id == merchant_id
        ).first()
    else:
        # Get most recent operation
        history = db.query(AutomationHistory).filter(
            AutomationHistory.merchant_id == merchant_id
        ).order_by(AutomationHistory.executed_at.desc()).first()
    
    if not history:
        return {
            "success": False,
            "error": "No operation found to undo"
        }
    
    # Restore previous state
    try:
        restored_count = 0
        
        if history.operation_type == "delete":
            # Cannot restore deleted products easily
            return {
                "success": False,
                "error": "Cannot undo delete operations. Products have been permanently removed."
            }
        
        for product_id, previous_values in history.previous_state.items():
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                product.stock = previous_values.get("stock", product.stock)
                product.updated_at = datetime.utcnow()
                restored_count += 1
        
        db.commit()
        
        # Delete history record
        db.delete(history)
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully undone operation '{history.operation_type}'. Restored {restored_count} products.",
            "restored_count": restored_count
        }
    
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Failed to undo operation: {str(e)}"
        }


async def _parse_automation_command(command: str, merchant_id: str) -> Dict:
    """Use LLM to parse automation command into structured action"""
    prompt = f"""
You are helping parse a user's automation command into a structured format.

User's command: "{command}"

Your task: Return ONLY a valid JSON object (no markdown, no explanations) with these fields:

1. "action" (required): Choose one:
   - "empty_stock" - set stock to 0
   - "update_stock" - change stock to a specific number
   - "delete" - remove products permanently

2. "filters" (required): An object with:
   - "search_query": what to search for in product name/description
   - "ingredient": specific ingredient if mentioned
   - "description": human-readable explanation of what products will be affected (REQUIRED)

3. "new_stock" (optional): new stock number if action is "update_stock"

Examples:

Input: "Kosongkan semua produk yang mengandung tepung"
Output: {{"action": "empty_stock", "filters": {{"search_query": "tepung", "ingredient": "tepung", "description": "produk yang mengandung tepung"}}}}

Input: "Hapus semua roti isi daging"
Output: {{"action": "delete", "filters": {{"search_query": "roti isi daging", "ingredient": "daging", "description": "roti isi daging"}}}}

Input: "Update stok kopi menjadi 50"
Output: {{"action": "update_stock", "filters": {{"search_query": "kopi", "description": "produk kopi"}}, "new_stock": 50}}

IMPORTANT: Always include the "description" field in filters. Return ONLY the JSON object.
"""
    
    try:
        response = await generate_text(prompt)
        # Extract JSON from response
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        if response.startswith("```"):
            response = response.replace("```", "").strip()
        
        parsed = json.loads(response)
        
        # Add fallback description if missing
        if "filters" in parsed and "description" not in parsed["filters"]:
            search_query = parsed["filters"].get("search_query", "")
            ingredient = parsed["filters"].get("ingredient", "")
            parsed["filters"]["description"] = search_query or ingredient or "produk yang dimaksud"
        
        # Validate schema
        validate(parsed, automation_schema)
        parsed["success"] = True
        return parsed

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON response: {e}. Response was: {response}")
        return {
            "success": False,
            "error": "Maaf, saya belum bisa memahami perintah tersebut dengan baik. Bisa diulang dengan lebih spesifik? Misalnya: 'Kosongkan stok semua produk roti' atau 'Hapus produk yang mengandung tepung'"
        }
    except ValidationError as e:
        logger.error(f"LLM response validation failed: {e}")
        return {
            "success": False,
            "error": "Hmm, saya kurang paham maksud perintahnya. Coba jelaskan lebih detail produk mana yang ingin diubah. Contoh: 'Hapus semua roti' atau 'Kosongkan stok produk tepung'"
        }
    except Exception as e:
        logger.error(f"Unexpected error in automation parsing: {e}")
        return {
            "success": False,
            "error": "Maaf, terjadi kesalahan saat memproses perintah. Bisa coba lagi atau gunakan kata-kata yang lebih sederhana?"
        }


async def _extract_stock_value(command: str) -> int:
    """Extract stock value from command if updating stock"""
    # Simple extraction - look for numbers
    import re
    numbers = re.findall(r'\d+', command)
    return int(numbers[0]) if numbers else 0


async def _find_affected_products(
    db: Session,
    merchant_id: str,
    filters: Dict
) -> List[Product]:
    """Find products that match the given filters"""
    query = db.query(Product).filter(Product.merchant_id == int(merchant_id))
    
    # Apply filters
    search_query = filters.get("search_query", "")
    ingredient = filters.get("ingredient", "")
    
    if search_query:
        # Search in name, description, category, or ingredients
        query = query.filter(
            (Product.name.ilike(f"%{search_query}%")) |
            (Product.description.ilike(f"%{search_query}%")) |
            (Product.category.ilike(f"%{search_query}%")) |
            (Product.ingredients.ilike(f"%{search_query}%"))
        )
    
    if ingredient:
        # Search specifically in ingredients field
        query = query.filter(Product.ingredients.ilike(f"%{ingredient}%"))
    
    return query.all()


def get_automation_history(
    db: Session,
    merchant_id: str,
    limit: int = 10
) -> List[Dict]:
    """Get automation history for a merchant"""
    history = db.query(AutomationHistory).filter(
        AutomationHistory.merchant_id == merchant_id
    ).order_by(AutomationHistory.executed_at.desc()).limit(limit).all()
    
    return [
        {
            "id": h.id,
            "operation_type": h.operation_type,
            "command": h.command,
            "affected_count": len(h.affected_product_ids),
            "executed_at": h.executed_at.isoformat(),
            "can_undo": h.operation_type != "delete"
        }
        for h in history
    ]
