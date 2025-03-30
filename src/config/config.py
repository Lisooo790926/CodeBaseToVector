from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Google Cloud settings (optional for testing)
    GOOGLE_CLOUD_PROJECT: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # Qdrant settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: Optional[int] = 6334
    QDRANT_COLLECTION_NAME: Optional[str] = None
    
    # Code parsing settings
    MAX_FILE_SIZE: int = 1000  # lines, placeholder for user input
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra fields in .env file

settings = Settings() 