# API Testing Commands

## Test Product CRUD via Chat

### 1. List Products
```bash
curl.exe -X POST http://localhost:8000/chatbot/message ^
-H "Content-Type: application/json" ^
-d "{\"merchant_id\": \"1\", \"message\": \"Tampilkan semua produk saya\"}"
```

### 2. Add Product
```bash
curl.exe -X POST http://localhost:8000/chatbot/message ^
-H "Content-Type: application/json" ^
-d "{\"merchant_id\": \"1\", \"message\": \"Tambahkan produk Roti Tawar harga 15000 stok 50\"}"
```

### 3. Edit Product
```bash
curl.exe -X POST http://localhost:8000/chatbot/message ^
-H "Content-Type: application/json" ^
-d "{\"merchant_id\": \"1\", \"message\": \"Ubah harga Roti Tawar jadi 12000\"}"
```

### 4. Delete Product
```bash
curl.exe -X POST http://localhost:8000/chatbot/message ^
-H "Content-Type: application/json" ^
-d "{\"merchant_id\": \"1\", \"message\": \"Hapus produk Roti Tawar\"}"
```

## Test Automation

### 5. Preview Automation
```bash
curl.exe -X POST http://localhost:8000/chatbot/automation/preview ^
-H "Content-Type: application/json" ^
-d "{\"merchant_id\": \"1\", \"command\": \"Kosongkan semua produk yang mengandung tepung\"}"
```

### 6. Execute Automation
```bash
curl.exe -X POST http://localhost:8000/chatbot/automation/execute ^
-H "Content-Type: application/json" ^
-d "{\"merchant_id\": \"1\", \"command\": \"Kosongkan semua produk yang mengandung tepung\", \"confirmed\": true}"
```

## Test Chat History

### 7. Get Chat History
```bash
curl.exe -X GET "http://localhost:8000/chatbot/chat/history?merchant_id=1&limit=20"
```

### 8. Get Automation History
```bash
curl.exe -X GET "http://localhost:8000/chatbot/automation/history?merchant_id=1&limit=10"
```

## Test Sync

### 9. Sync Products to Qdrant
```bash
curl.exe -X POST "http://localhost:8000/chatbot/automation/sync?merchant_id=1"
```

---

## Using PowerShell (Alternative)

If curl.exe doesn't work, use PowerShell:

```powershell
# List Products
$body = @{
    merchant_id = "1"
    message = "Tampilkan semua produk saya"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chatbot/message" -Method POST -Body $body -ContentType "application/json"
```

```powershell
# Add Product
$body = @{
    merchant_id = "1"
    message = "Tambahkan produk Roti Tawar harga 15000 stok 50"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chatbot/message" -Method POST -Body $body -ContentType "application/json"
```

```powershell
# Get Chat History
Invoke-RestMethod -Uri "http://localhost:8000/chatbot/chat/history?merchant_id=1&limit=20" -Method GET
```
