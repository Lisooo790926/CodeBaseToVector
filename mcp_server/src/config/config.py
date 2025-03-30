from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    # Qdrant settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # Code parsing settings
    MAX_FILE_SIZE: int = 1000  # lines, placeholder for user input
    
    class Config:
        env_file = ".env"

settings = Settings() 