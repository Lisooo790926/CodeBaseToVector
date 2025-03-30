from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Main configuration settings for the MCP server.
    
    Attributes:
        MAX_FILE_SIZE: Maximum file size to process (in lines)
        GOOGLE_API_KEY: Google API key
        QDRANT_HOST: Qdrant host
        QDRANT_PORT: Qdrant port
        QDRANT_GRPC_PORT: Qdrant gRPC port
    """
    
    MAX_FILE_SIZE: int = 1000
    
    # Google Cloud settings (optional for testing)
    GOOGLE_API_KEY: Optional[str] = None
    
    # Qdrant settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: Optional[int] = 6334
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow extra fields in .env file

settings = Settings() 