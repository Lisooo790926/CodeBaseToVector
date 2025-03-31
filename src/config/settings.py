import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # Google API settings
    GOOGLE_API_KEY: str
    
    # Qdrant settings
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "qdrant")
    QDRANT_PORT: int = os.getenv("QDRANT_PORT", 6333)
    QDRANT_GRPC_PORT: Optional[int] = os.getenv("QDRANT_GRPC_PORT", 6334)
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "code_vectors")
    VECTOR_SIZE: int = os.getenv("VECTOR_SIZE", 3072)
    
    # Project settings
    DEFAULT_LANGUAGE: str = "java"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields in environment variables


# Global settings instance
settings = Settings() 