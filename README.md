# Smartgement - Smart Product Management System

Sistem manajemen produk pintar untuk UMKM dengan AI chatbot, automasi, dan analisis risiko.

##  Features

- **AI Chatbot**: Kelola produk dengan natural language (Bahasa Indonesia)
- **Product CRUD**: Tambah, edit, hapus, lihat produk via chat
- **Automation**: Operasi bulk pada produk (kosongkan stok, hapus batch, dll)
- **Risk Analysis**: Deteksi produk berisiko tinggi, expired, low stock
- **Conversation Memory**: Chatbot mengingat 7 pesan terakhir untuk konteks
- **Authentication**: Protected routes, user management
- **Profile Management**: Edit profil dan ubah password

##  Project Structure

```
smartgement/
├── backend/           # Go (Fiber v2) - API Gateway & Auth
├── aiservices/        # Python (FastAPI) - AI & Chatbot
├── frontend/          # Nuxt.js - User Interface
└── README.md
```

##  Technology Stack

### Backend (Go)
- **Framework**: Fiber v2
- **ORM**: GORM
- **Database**: MySQL
- **Auth**: JWT

### AI Services (Python)
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **LLM**: OpenAI GPT-4o-mini
- **Database**: MySQL

### Frontend (Nuxt.js)
- **Framework**: Nuxt 4
- **UI**: TailwindCSS + Custom CSS
- **State**: Composables (useAuth, useApi)

##  Prerequisites

- **Go** 1.21+
- **Python** 3.10+
- **Node.js** 18+
- **MySQL** 8.0+

## 🔧 Installation

### 1. Database Setup

```sql
CREATE DATABASE smartgement;
```

### 2. Backend (Go)

```bash
cd backend
go mod download
cp .env.example .env  # Configure database
go run cmd/main.go
```

**Port**: 8080

### 3. AI Services (Python)

```bash
cd aiservices
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY

python run_server.py
```

**Port**: 8000

### 4. Frontend (Nuxt)

```bash
cd smartgement-fe
npm install
npm run dev
```

**Port**: 3000

##  Environment Variables

### Backend (.env)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=smartgement
JWT_SECRET=your-secret-key
```

### AI Services (.env)
```env
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/smartgement
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

### Frontend (nuxt.config.ts)
```typescript
runtimeConfig: {
  public: {
    apiBase: 'http://localhost:8080/api',
    aiBase: 'http://localhost:8000',
  }
}
```

##  Usage

### Chat Commands (Bahasa Indonesia)

**Product CRUD:**
```
- "Tampilkan semua produk saya"
- "Tambahkan produk Roti Tawar harga 15000 stok 50"
- "Ubah harga Roti Tawar jadi 12000"
- "Hapus produk Roti Tawar"
```

**Automation:**
```
- "Kosongkan semua produk yang mengandung tepung"
- "Hapus semua produk expired"
- "Update stok semua roti jadi 100"
```

**Analysis:**
```
- "Produk apa yang berisiko tinggi?"
- "Tampilkan produk yang hampir expired"
```

### API Endpoints

#### Go Backend (8080)
```
POST   /api/auth/login
POST   /api/auth/register
GET    /api/products
POST   /api/products
PUT    /api/products/:id
DELETE /api/products/:id
GET    /api/users/:id
PUT    /api/users/:id
PUT    /api/users/:id/password
```

#### AI Services (8000)
```
POST   /chatbot/message
POST   /chatbot/automation/preview
POST   /chatbot/automation/execute
GET    /chatbot/chat/history
GET    /risk/assess/:product_id
GET    /risk/high-risk
```

##  Architecture

### Data Flow

```
User (Frontend)
  ↓
Go Backend (Auth, Products)
  ↓
Python AI (Chatbot, Analysis)
  ↓
MySQL Database
```

### Authentication Flow

```
1. User login → Go Backend
2. JWT token generated
3. Token stored in cookie
4. Protected routes check auth middleware
5. API calls include JWT in header
```

### Chat Flow

```
1. User sends message → Frontend
2. Frontend sends last 7 messages as context
3. AI Services classify intent
4. Route to appropriate handler
5. Database operations (if needed)
6. Return response with suggested actions
7. Frontend displays messages
```

##  Key Features Explained


### 1. Conversation Memory

Chatbot ingat 7 pesan terakhir:
```typescript
conversationHistory = messages.slice(-8, -1)
```

Benefit: Follow-up questions work naturally.

### 2. Smart Automation

Preview before execute:
```
1. User: "Kosongkan produk tepung"
2. AI: Shows preview (2 products affected)
3. User clicks "Eksekusi"
4. API executes automation
5. Shows success (2 products updated)
```

##  Testing

### Manual Testing

**Chat Interface:**
```bash
# Start all services
npm run dev  # Frontend
go run cmd/main.go  # Backend
python run_server.py  # AI Services

# Test at http://localhost:3000/chat
```

**API Testing:**
```powershell
# List products
$body = @{ merchant_id = "1"; message = "Tampilkan produk" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chatbot/message" -Method POST -Body $body -ContentType "application/json"
```

## � Database Schema

### Products
```sql
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  merchant_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  stock INT DEFAULT 0,
  price DECIMAL(10,2),
  ingredients TEXT,
  category VARCHAR(100),
  expiration_date DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Chat History
```sql
CREATE TABLE chat_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  merchant_id VARCHAR(50) NOT NULL,
  user_message TEXT NOT NULL,
  ai_response TEXT,
  intent VARCHAR(50),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

##  Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error
```bash
# Check MySQL is running
mysql -u root -p

# Verify database exists
SHOW DATABASES;
```

### OpenAI API Error
```bash
# Verify API key in .env
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

##  Deployment

### Production Checklist

- [✓] Set production environment variables
- [✓] Use secure JWT secret
- [✓] Enable HTTPS
- [✓] Configure CORS properly
- [✓] Set up database backups
- [✓] Monitor API usage (OpenAI)
- [✓] Set up error logging
- [✓] Configure rate limiting


- OpenAI for GPT-4 API
- Nuxt.js team
- FastAPI team
- Fiber team

##  Support

For support, email synchronizeteams88@gmail.com or open an issue.

---

**Built with ❤️ for Indonesian UMKM**
