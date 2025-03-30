from typing import List, Dict, Optional, Any
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from type_definitions.code_types import CodeVectorMetadata

class VectorStorageService:
    """Service for managing vector storage operations using Qdrant."""

    def __init__(self, host: str, port: int):
        """Initialize the vector storage service.
        
        Args:
            host (str): Qdrant server host
            port (int): Qdrant server port
        """
        self.client = QdrantClient(host=host, port=port)
        self.logger = logging.getLogger(__name__)

    def create_collection(self, collection_name: str, vector_size: int = 768) -> bool:
        """Create a new collection for storing vectors.
        
        Args:
            collection_name (str): Name of the collection
            vector_size (int): Size of the vectors to be stored
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.debug(f"Creating collection {collection_name} with vector size {vector_size}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            self.logger.info(f"Collection {collection_name} created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create collection {collection_name}: {str(e)}")
            return False

    def store_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        metadata_list: List[CodeVectorMetadata]
    ) -> bool:
        """Store vectors with their metadata in the specified collection.
        
        Args:
            collection_name (str): Name of the collection
            vectors (List[List[float]]): List of vectors to store
            metadata_list (List[CodeVectorMetadata]): List of metadata for each vector
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.debug(f"Storing vectors in collection {collection_name}")
            points = [
                PointStruct(
                    id=i,
                    vector=vector,
                    payload=metadata.model_dump()
                )
                for i, (vector, metadata) in enumerate(zip(vectors, metadata_list))
            ]
            
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            self.logger.info(f"Vectors stored in collection {collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to store vectors in collection {collection_name}: {str(e)}")
            return False

    def search_vectors(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5,
        project_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in the collection.
        
        Args:
            collection_name (str): Name of the collection
            query_vector (List[float]): Query vector to search for
            limit (int): Maximum number of results to return
            project_name (Optional[str]): Filter results by project name
            
        Returns:
            List[Dict[str, Any]]: List of search results with metadata
        """
        try:
            search_params = {}
            if project_name:
                search_params["filter"] = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="project_name",
                            match=models.MatchValue(value=project_name)
                        )
                    ]
                )

            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                **search_params
            )
            
            self.logger.debug(f"Search results: {results}")
            return [
                {
                    "score": hit.score,
                    "metadata": hit.payload
                }
                for hit in results
            ]
        except Exception as e:
            self.logger.error(f"Failed to search vectors in collection {collection_name}: {str(e)}")
            return []

    def delete_project_vectors(self, collection_name: str, project_name: str) -> bool:
        """Delete all vectors belonging to a specific project.
        
        Args:
            collection_name (str): Name of the collection
            project_name (str): Name of the project to delete vectors for
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.delete(
                collection_name=collection_name,
                points_selector=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="project_name",
                            match=models.MatchValue(value=project_name)
                        )
                    ]
                )
            )
            self.logger.info(f"Vectors deleted for project {project_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete vectors for project {project_name}: {str(e)}")
            return False

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists.
        
        Args:
            collection_name (str): Name of the collection to check
            
        Returns:
            bool: True if collection exists, False otherwise
        """
        try:
            collections = self.client.get_collections()
            return any(collection.name == collection_name for collection in collections.collections)
        except Exception as e:
            self.logger.error(f"Failed to check collection existence: {str(e)}")
            return False 