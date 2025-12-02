from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import embeddings, ai_generate, risk, products, trends, chatbot, collections
from app.database import init_db
from app.config import settings

app = FastAPI(
    title="AI Product Management Services",
    description="LLM, RAG, Qdrant services for UMKM with Product Management, Trend Analysis, and Chatbot Automation",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(trends.router, prefix="/trends", tags=["Trends"])
app.include_router(risk.router, prefix="/risk", tags=["Risk Analysis"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(embeddings.router, prefix="/embeddings", tags=["Embeddings"])
app.include_router(collections.router, prefix="/collections", tags=["Collections"])
app.include_router(ai_generate.router, prefix="/ai", tags=["AI Generation"])

@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db()

@app.get("/")
def root():
    return {
        "message": "AI Product Management Services Running",
        "version": "2.0.0",
        "features": [
            "Product Management",
            "Trend Analysis & Prediction",
            "Risk Assessment",
            "AI Chatbot with Automation",
            "Semantic Search"
        ]
    }
