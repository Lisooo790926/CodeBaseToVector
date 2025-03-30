from typing import Optional
from src.config.settings import settings
from src.services.vector_storage import VectorStorageService
from src.services.vector_embedding import VectorEmbeddingService
from src.services.code_parser import JavaCodeParser


class ServiceFactory:
    """Factory for creating and managing service instances."""
    
    _vector_storage: Optional[VectorStorageService] = None
    _vector_embedding: Optional[VectorEmbeddingService] = None
    _java_code_parser: Optional[JavaCodeParser] = None
    
    @classmethod
    def get_vector_storage(cls) -> VectorStorageService:
        """Get or create VectorStorageService instance."""
        if cls._vector_storage is None:
            cls._vector_storage = VectorStorageService(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )
            # Ensure the default collection exists
            if not cls._vector_storage.collection_exists(settings.QDRANT_COLLECTION_NAME):
                cls._vector_storage.create_collection(
                    collection_name=settings.QDRANT_COLLECTION_NAME,
                    vector_size=settings.VECTOR_SIZE
                )
        return cls._vector_storage
    
    @classmethod
    def get_vector_embedding(cls) -> VectorEmbeddingService:
        """Get or create VectorEmbeddingService instance."""
        if cls._vector_embedding is None:
            cls._vector_embedding = VectorEmbeddingService()
        return cls._vector_embedding
    
    @classmethod
    def get_java_code_parser(cls) -> JavaCodeParser:
        """Get or create JavaCodeParser instance."""
        if cls._java_code_parser is None:
            cls._java_code_parser = JavaCodeParser()
        return cls._java_code_parser 