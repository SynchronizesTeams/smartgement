"""
Transaction Automation Service
Handles transaction creation via natural language
"""
from sqlalchemy.orm import Session
from app.models.product import Product
from app.services.llm_client import generate_text
import json
import re
from typing import Dict, List

class TransactionAutomationService:
    
    async def parse_transaction_request(self, description: str) -> Dict:
        """Parse transaction from natural language"""
        prompt = f"""
        Parse this transaction request into JSON format:
        "{description}"
        
        Extract:
        - customer_name (string, jika tidak ada gunakan "Walk-in")
        - items (array of objects with: product_name, quantity)
        
        Return ONLY valid JSON:
        {{
            "customer_name": "...",
            "items": [
                {{"product_name": "...", "quantity": ...}}
            ]
        }}
        """
        
        try:
            response = await generate_text(prompt)
            # Clean response to get JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return {
                    "success": True,
                    "data": parsed
                }
        except Exception as e:
            pass
        
        # Fallback parser using regex
        return self.fallback_parser(description)
    
    def fallback_parser(self, description: str) -> Dict:
        """Simple fallback parser using regex"""
        # Try to find customer name
        customer_match = re.search(r'(?:untuk|atas nama|customer)\s+([A-Za-z\s]+)', description, re.IGNORECASE)
        customer_name = customer_match.group(1).strip() if customer_match else "Walk-in"
        
        # Try to find items (e.g., "2 Roti Tawar", "3 Susu")
        items = []
        item_pattern = r'(\d+)\s+([A-Za-z\s]+?)(?:\s+(?:Rp|rp|dan|,|dengan|$))'
        matches = re.findall(item_pattern, description)
        
        for qty, name in matches:
            items.append({
                "product_name": name.strip(),
                "quantity": int(qty)
            })
        
        return {
            "success": len(items) > 0,
            "data": {
                "customer_name": customer_name,
                "items": items
            }
        }
    
    async def match_products(self, db: Session, merchant_id: str, items: List[Dict]) -> List[Dict]:
        """Match product names to database products"""
        products = db.query(Product).filter(Product.merchant_id == merchant_id).all()
        
        matched_items = []
        for item in items:
            product_name = item["product_name"].lower()
            
            # Find best match
            best_match = None
            best_score = 0
            
            for product in products:
                # Simple scoring: count matching words
                db_name = product.name.lower()
                matching_words = sum(1 for word in product_name.split() if word in db_name)
                score = matching_words / max(len(product_name.split()), 1)
                
                if score > best_score:
                    best_score = score
                    best_match = product
            
            if best_match and best_score > 0.3:  # Threshold for match
                matched_items.append({
                    "product_id": best_match.id,
                    "product_name": best_match.name,
                    "quantity": item["quantity"],
                    "price": best_match.price,
                    "matched_score": best_score
                })
        
        return matched_items
    
    async def create_transaction_data(self, db: Session, merchant_id: str, description: str) -> Dict:
        """Parse description and prepare transaction data"""
        # Parse the request
        parse_result = await self.parse_transaction_request(description)
        
        if not parse_result["success"]:
            return {
                "success": False,
                "error": "Tidak dapat memahami format transaksi. Contoh: 'Tambahkan transaksi untuk Budi dengan 2 Roti Tawar dan 3 Susu'"
            }
        
        data = parse_result["data"]
        
        # Match products
        matched_items = await self.match_products(db, merchant_id, data["items"])
        
        if not matched_items:
            return {
                "success": False,
                "error": "Tidak ada produk yang cocok ditemukan. Pastikan nama produk sudah terdaftar."
            }
        
        # Calculate total
        total_amount = sum(item["price"] * item["quantity"] for item in matched_items)
        
        return {
            "success": True,
            "transaction_data": {
                "customer_name": data["customer_name"],
                "payment_method": "cash",  # Default
                "items": [
                    {
                        "product_id": item["product_id"],
                        "quantity": item["quantity"]
                    }
                    for item in matched_items
                ],
                "total_amount": total_amount
            },
            "preview": {
                "customer": data["customer_name"],
                "items": matched_items,
                "total": total_amount
            }
        }
    
    async def batch_add_products(self, db: Session, merchant_id: str, description: str) -> Dict:
        """Add multiple products from package/batch description"""
        prompt = f"""
        Parse this product batch request:
        "{description}"
        
        Extract product details. Return JSON array:
        [
            {{"name": "...", "price": ..., "stock": ..., "category": "..."}}
        ]
        
        Generate reasonable prices and stock if not specified.
        If description mentioned ("deskripsi otomatis" or "auto description"), set generate_description: true
        """
        
        try:
            response = await generate_text(prompt)
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                products = json.loads(json_match.group())
                return {
                    "success": True,
                    "products": products
                }
        except:
            pass
        
        return {
            "success": False,
            "error": "Tidak dapat memparse permintaan batch produk"
        }

transaction_automation_service = TransactionAutomationService()
