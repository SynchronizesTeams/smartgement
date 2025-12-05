# Merchant Product Management Backend

A complete Go backend boilerplate built with Fiber v2, GORM, and PostgreSQL for merchant product management with AI automation and semantic search support.

## Tech Stack

- **Go**: 1.22+
- **Framework**: Fiber v2
- **ORM**: GORM
- **Database**: PostgreSQL
- **Vector DB**: Qdrant (placeholder integration)
- **Environment**: .env configuration

## Features

✅ **Product Management**: Full CRUD operations for merchant products  
✅ **Chat Automation**: Placeholder endpoints for AI-powered chat commands  
✅ **Semantic Search**: Qdrant client structure for embedding-based search  
✅ **Modular Architecture**: Clean separation of controllers, services, and routes  
✅ **JWT Authentication**: Middleware placeholder for secure endpoints  
✅ **Auto Migrations**: GORM AutoMigrate for database schema management  

## Project Structure

```
backend/
├── cmd/
│   └── main.go                 # Application entry point
├── config/
│   └── database.go             # Database configuration
├── controllers/
│   ├── product_controller.go   # Product REST handlers
│   └── chat_controller.go      # Chat command handlers
├── middlewares/
│   └── auth.go                 # JWT authentication (placeholder)
├── models/
│   ├── user.go                 # User model
│   ├── product.go              # Product model
│   └── sync_job.go             # Sync job model
├── routes/
│   ├── product_routes.go       # Product route definitions
│   └── chat_routes.go          # Chat route definitions
├── services/
│   ├── product_service.go      # Product business logic
│   └── chat_service.go         # Chat service (placeholder)
├── qdrant/
│   ├── client.go               # Qdrant client (placeholder)
│   └── vector_store.go         # Vector operations (placeholder)
├── utils/
│   └── response.go             # Response helpers
├── .env.example                # Environment variables template
├── go.mod                      # Go module definition
└── go.sum                      # Dependency checksums
```

## Database Schema

### Users
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `password` (String, Hashed)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Products
- `id` (UUID, Primary Key)
- `merchant_id` (UUID, Foreign Key → users.id)
- `name` (String)
- `description` (Text)
- `stock` (Integer)
- `price` (Decimal)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Sync Jobs
- `id` (UUID, Primary Key)
- `merchant_id` (UUID, Foreign Key → users.id)
- `job_type` (String)
- `status` (String)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

## Setup Instructions

### Prerequisites

- Go 1.22 or higher
- PostgreSQL database
- Qdrant (optional, for future semantic search)

### Installation

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database credentials:
   ```env
   DB_HOST=localhost
   DB_USER=postgres
   DB_PASS=yourpassword
   DB_NAME=merchant_db
   DB_PORT=5432
   JWT_SECRET=yourSecretKey
   QDRANT_URL=http://localhost:6333
   ```

3. **Install dependencies** (already done during setup):
   ```bash
   go mod tidy
   ```

4. **Create PostgreSQL database**:
   ```sql
   CREATE DATABASE merchant_db;
   ```

### Running the Server

Start the development server:

```bash
cd backend && go run cmd/main.go
```

The server will start on port **3000** by default. Auto-migrations will run automatically on startup.

### Building for Production

Build the executable:

```bash
go build -o backend.exe ./cmd/main.go
```

Run the compiled binary:

```bash
./backend.exe
```

## API Endpoints

### Health Check
- **GET** `/health` - Server health status

### Products (Protected)
- **GET** `/api/products` - List all products for merchant
- **GET** `/api/products/:id` - Get product by ID
- **POST** `/api/products` - Create new product
- **PUT** `/api/products/:id` - Update product
- **DELETE** `/api/products/:id` - Delete product

### Chat Automation (Protected)
- **POST** `/api/chat/command` - Process chat command (placeholder)
- **GET** `/api/chat/history` - Retrieve chat history (placeholder)

### Authentication

All `/api/*` routes require authentication via the `Authorization` header (JWT - placeholder implementation).

## Development Notes

### Placeholder Components

The following components are placeholders ready for implementation:

1. **JWT Authentication**: `middlewares/auth.go` - Add token verification logic
2. **Qdrant Integration**: `qdrant/client.go` and `qdrant/vector_store.go` - Implement vector operations
3. **Chat Service**: `services/chat_service.go` - Connect to AI services

### Integration with AI Services

This backend is designed to work with the AI services in the `aiservices/` folder. The chat service and Qdrant integration provide the foundation for:

- Product trend analysis
- Risk assessment
- Expiration tracking
- Semantic product search
- Automated task processing via chat

## Testing

Test health endpoint:
```bash
curl http://localhost:3000/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

## Next Steps

1. Implement JWT token generation and verification
2. Connect Qdrant client to actual Qdrant instance
3. Integrate chat service with AI services (FastAPI)
4. Add product embedding generation for semantic search
5. Implement user authentication endpoints
6. Add comprehensive error handling and validation

## License

MIT
