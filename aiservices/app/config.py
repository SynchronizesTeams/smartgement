from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""
    
    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    
    # OpenAI Configuration
    openai_api_key: str
    openai_api_base: str = "https://api.openai.com/v1"
    
    # Database Configuration
    database_url: str = "sqlite:///./products.db"
    
    # Application Settings
    app_name: str = "AI Product Management Services"
    debug: bool = False
    cors_origins: list[str] = ["*"]
    
    # Embedding Configuration
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    
    # LLM Configuration
    llm_model: str = "gpt-4o-mini"
    max_tokens: int = 1000
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
