from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Google API settings
    GOOGLE_API_KEY: str
    
    # Qdrant settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: Optional[int] = 6334
    QDRANT_COLLECTION_NAME: str = "code_vectors"
    VECTOR_SIZE: int = 3072
    
    # Project settings
    DEFAULT_LANGUAGE: str = "java"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields in environment variables


# Global settings instance
settings = Settings() 