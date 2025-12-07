"""
Business Education Service
Provides context-aware business tips and best practices
"""
from sqlalchemy.orm import Session
from app.models.product import Product
from app.services.llm_client import generate_text
from typing import List, Dict
import json

class EducationService:
    
    def detect_business_type(self, products: List[Product]) -> str:
        """Detect business type from product catalog"""
        if not products:
            return "general"
        
        # Analyze product names to detect business type
        product_names = " ".join([p.name.lower() for p in products[:20]])
        
        keywords = {
            "food": ["roti", "nasi", "makan", "kue", "snack", "minum", "susu", "telur"],
            "retail": ["baju", "celana", "sepatu", "tas", "aksesoris"],
            "grocery": ["sayur", "buah", "beras", "gula", "minyak", "bumbu"],
            "pharmacy": ["obat", "vitamin", "kesehatan", "medis"],
            "electronics": ["hp", "laptop", "charger", "kabel", "gadget"]
        }
        
        for biz_type, keys in keywords.items():
            if any(key in product_names for key in keys):
                return biz_type
        
        return "general"
    
    async def get_business_tips(self, db: Session, merchant_id: str) -> Dict:
        """Get contextual business tips"""
        # Get merchant products
        products = db.query(Product).filter(Product.merchant_id == merchant_id).all()
        
        if not products:
            return {
                "tips": [
                    "Mulai tambahkan produk ke inventori Anda",
                    "Kategorikan produk dengan baik untuk memudahkan manajemen",
                    "Tetapkan harga yang kompetitif"
                ],
                "business_type": "new_business"
            }
        
        business_type = self.detect_business_type(products)
        total_products = len(products)
        low_stock = len([p for p in products if p.stock < 10])
        
        # Generate contextual tips using LLM
        prompt = f"""
        Berikan 3-5 tips bisnis praktis dan spesifik untuk toko dengan karakteristik:
        - Jenis bisnis: {business_type}
        - Jumlah produk: {total_products}
        - Produk stok rendah: {low_stock}
        
        Format: JSON array of strings, bahasa Indonesia, praktis dan actionable.
        Contoh: ["Tip 1...", "Tip 2...", ...]
        """
        
        try:
            response = await generate_text(prompt)
            # Parse JSON from response
            tips = json.loads(response.strip())
            if not isinstance(tips, list):
                tips = [response]
        except:
            # Fallback tips by business type
            tips = self.get_fallback_tips(business_type)
        
        return {
            "tips": tips,
            "business_type": business_type,
            "total_products": total_products
        }
    
    def get_fallback_tips(self, business_type: str) -> List[str]:
        """Get fallback tips when LLM fails"""
        tips_db = {
            "food": [
                "🍞 Pastikan rotasi stok FIFO (First In First Out) untuk produk makanan",
                "⏰ Tawarkan promo khusus untuk jam-jam sepi",
                "📦 Bundling produk populer bisa meningkatkan penjualan hingga 30%",
                "🌡️ Monitor suhu penyimpanan produk yang mudah rusak"
            ],
            "grocery": [
                "🛒 Tempatkan produk kebutuhan pokok di bagian belakang toko",
                "💰 Buat program loyalitas untuk pelanggan tetap",
                "📊 Analisis produk terlaris dan tambah stok 20% lebih banyak",
                "🎯 Tawarkan paket hemat untuk pembelian grosir"
            ],
            "retail": [
                "👕 Display produk dengan visual menarik untuk meningkatkan penjualan",
                "📸 Dokumentasikan produk dengan foto berkualitas",
                "🏷️ Gunakan strategi harga psikologis (Rp99.000 vs Rp100.000)",
                "🎁 Sediakan pilihan gift wrapping untuk meningkatkan nilai jual"
            ],
            "general": [
                "📈 Pantau tren penjualan mingguan dan bulanan",
                "💡 Investasi dalam customer service yang baik",
                "📱 Manfaatkan media sosial untuk promosi gratis",
                "🎯 Fokus pada produk dengan margin keuntungan tinggi"
            ]
        }
        
        return tips_db.get(business_type, tips_db["general"])
    
    async def get_growth_strategy(self, db: Session, merchant_id: str) -> str:
        """Get personalized growth strategy"""
        products = db.query(Product).filter(Product.merchant_id == merchant_id).all()
        business_type = self.detect_business_type(products)
        
        total_value = sum(p.stock * p.price for p in products)
        avg_price = sum(p.price for p in products) / len(products) if products else 0
        
        prompt = f"""
        Buatkan strategi pertumbuhan bisnis singkat (3-4 kalimat) untuk toko {business_type} dengan:
        - Total nilai inventori: Rp{total_value:,.0f}
        - Rata-rata harga produk: Rp{avg_price:,.0f}
        - Jumlah produk: {len(products)}
        
        Fokus pada strategi praktis yang bisa diterapkan dalam 1-3 bulan.
        Bahasa Indonesia, professional namun friendly.
        """
        
        try:
            strategy = await generate_text(prompt)
            return strategy.strip()
        except:
            return f"Untuk mengembangkan bisnis {business_type} Anda, fokus pada: 1) Meningkatkan variasi produk berkualitas, 2) Membangun loyalitas pelanggan melalui service excellent, 3) Optimasi stok produk best-seller untuk maksimalkan profit."

education_service = EducationService()
