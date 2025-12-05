# AI Product Management Services

AI-powered product management and chatbot service untuk UMKM (Usaha Mikro, Kecil, dan Menengah) dengan fitur trend analysis, risk assessment, dan automation berbasis LLM.

## ✨ Features

### 1. Product Management with AI
- **CRUD Operations** - Kelola produk dengan mudah
- **Semantic Search** - Cari produk menggunakan deskripsi natural language
- **Vector Embeddings** - Produk diindex dengan Qdrant untuk pencarian yang lebih akurat

### 2. Trend Analysis & Prediction
- **Sales Tracking** - Record penjualan harian untuk analisis
- **Demand Forecasting** - Prediksi permintaan 7-30 hari ke depan
- **Seasonality Detection** - Deteksi pola musiman penjualan
- **Purchase Recommendations** - Rekomendasi jumlah pembelian optimal

### 3. Risk Management
- **Multi-Factor Risk Assessment**:
  - ⏰ Expiration Risk - Produk mendekati atau sudah expired
  - 📦 Stock Risk - Stok rendah berdasarkan demand
  - 📉 Trend Risk - Penurunan popularitas produk
  - 💰 Financial Risk - High-value inventory dengan turnover rendah
- **Risk Reports** - Laporan komprehensif produk berisiko tinggi

### 4. AI Chatbot with Automation
- **Natural Language Interface** - Tanya dan kelola produk dengan bahasa natural
- **Intent Classification** - Otomatis mengenali maksud user (query, automation, risk report)
- **Bulk Operations** - Automasi operasi massal dengan konfirmasi safety
- **Undo Capability** - Rollback operasi yang salah

Contoh automation:
- "Kosongkan semua produk yang mengandung tepung"
- "Hapus semua roti yang sudah expired"
- "Berapa penjualan minggu ini?"

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API Key
- Qdrant Cloud account (atau local Qdrant instance)

### Installation

1. **Clone dan navigasi ke project**
```bash
cd c:\Users\ihsan\VScodeProject\services
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Buat file `.env` di root project (sudah ada template):
```env
QDRANT_URL=https://your-qdrant-instance.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=sk-your_openai_api_key
DATABASE_URL=sqlite:///./products.db
```

4. **Run the server**
```bash
uvicorn app.main:app --reload
```

Server akan berjalan di `http://localhost:8000`

5. **Access API Documentation**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Usage Examples

### Product Management

**Create Product**
```bash
POST /products
{
  "merchant_id": "merchant_001",
  "name": "Roti Coklat",
  "description": "Roti manis dengan cokelat premium",
  "stock": 50,
  "price": 15000,
  "ingredients": "tepung terigu, cokelat, gula, mentega",
  "category": "bakery",
  "expiration_date": "2025-12-10T00:00:00"
}
```

**Semantic Search**
```bash
POST /products/search
{
  "merchant_id": "merchant_001",
  "query": "produk yang mengandung tepung",
  "limit": 10
}
  "limit": 10
}
```

**Get Raw Qdrant Data**
```bash
GET /products/qdrant?merchant_id=merchant_001&skip=0&limit=10
```
Returns raw payload data directly from Qdrant collection.

### Trend Analysis

**Record Sale**
```bash
POST /trends/record-sale
{
  "product_id": 1,
  "merchant_id": "merchant_001",
  "quantity": 10
}
```

**Get Trend Analysis**
```bash
GET /trends/analysis/1?days=30
```

**Demand Prediction**
```bash
GET /trends/predict/1
```

### Risk Assessment

**Assess Product Risk**
```bash
POST /risk/assess/1
```

**Get High-Risk Products**
```bash
GET /risk/high-risk?merchant_id=merchant_001
```

**Risk Report**
```bash
GET /risk/report/merchant_001
```

### Chatbot & Automation

**Send Message to Chatbot**
```bash
POST /chatbot/message
{
  "merchant_id": "merchant_001",
  "message": "Produk apa yang berisiko tinggi?"
}
```

**Preview Automation**
```bash
POST /chatbot/automation/preview
{
  "merchant_id": "merchant_001",
  "command": "Kosongkan semua produk yang mengandung tepung"
}
```

**Execute Automation**
```bash
POST /chatbot/automation/execute
{
  "merchant_id": "merchant_001",
  "command": "Kosongkan semua produk yang mengandung tepung",
  "confirmed": true
}
```

**Undo Operation**
```bash
POST /chatbot/automation/undo
{
  "merchant_id": "merchant_001"
}
```

## 🏗️ Project Structure

```
services/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database setup
│   ├── models/                 # SQLAlchemy models
│   │   └── product.py
│   ├── schemas/                # Pydantic schemas
│   │   └── product.py
│   ├── routers/                # API endpoints
│   │   ├── products.py
│   │   ├── trends.py
│   │   ├── risk.py
│   │   ├── chatbot.py
│   │   ├── embeddings.py
│   │   └── ai_generate.py
│   ├── services/               # Business logic
│   │   ├── product_service.py
│   │   ├── trend_service.py
│   │   ├── risk_services.py
│   │   ├── automation_service.py
│   │   ├── chatbot_service.py
│   │   ├── qdrant_setup.py
│   │   ├── llm_client.py
│   │   └── rag_services.py
│   └── tests/                  # Test files
├── requirements.txt
├── .env
└── README.md
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## 🔧 Configuration

Configuration menggunakan `pydantic-settings` yang load dari `.env`:

- `QDRANT_URL` - Qdrant instance URL
- `QDRANT_API_KEY` - Qdrant API key
- `OPENAI_API_KEY` - OpenAI API key
- `DATABASE_URL` - Database connection string (default: SQLite)
- `EMBEDDING_MODEL` - Model untuk embeddings (default: text-embedding-3-small)
- `LLM_MODEL` - Model untuk text generation (default: gpt-4o-mini)

## 💡 Use Cases

### Example 1: Trend-Based Inventory Management
```
1. Record daily sales untuk "Roti Coklat"
2. Analyze trends untuk identifikasi peak dates
3. Get demand prediction
4. Receive purchase recommendations
```

### Example 2: Risk Mitigation
```
1. Run risk report untuk semua produk
2. Identify produk dengan expiration risk
3. Chatbot automation: "Diskon 50% untuk semua produk yang expired dalam 3 hari"
```

### Example 3: Semantic Product Search
```
1. User bertanya: "Apa saja produk yang pakai tepung?"
2. Chatbot menggunakan vector search di Qdrant
3. Return: Gorengan, Roti Coklat, Kue Kering, dll
4. Optional: Bulk operation jika diperlukan
```

## 📝 Notes

- **Database**: Default menggunakan SQLite untuk development. Untuk production, gunakan PostgreSQL dengan update `DATABASE_URL`
- **Qdrant**: Setiap merchant memiliki collection terpisah: `merchant_{merchant_id}`
- **Safety**: Automation operations yang affect >5 produk require konfirmasi
- **Undo**: Delete operations tidak bisa di-undo, hanya update operations

## 🔐 Security Considerations

- ✅ API keys tidak di-hardcode (menggunakan .env)
- ✅ Automation requires confirmation untuk operasi destructive
- ✅ Preview mode sebelum execute automation
- ✅ Undo capability untuk rollback
- ⚠️ Belum ada authentication - tambahkan auth middleware untuk production

## 🚧 Future Enhancements

- [ ] User authentication & authorization
- [ ] Rate limiting untuk LLM calls
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Webhook notifications untuk high-risk alerts
- [ ] Export functionality untuk reports
- [ ] Batch import products dari CSV/Excel

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Feel free to submit issues or pull requests.
