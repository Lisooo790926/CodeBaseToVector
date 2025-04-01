from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from services.service_factory import ServiceFactory
from type_definitions.code_types import CodeDataForVector, CodeVectorMetadata
from config.settings import settings


class CodebaseService:
    """Main service for Codebase functionality."""
    
    def __init__(self):
        """Initialize Codebase service."""
        self.logger = logging.getLogger(__name__)
        self.vector_storage = ServiceFactory.get_vector_storage()
        self.vector_embedding = ServiceFactory.get_vector_embedding()
        self.java_code_parser = ServiceFactory.get_java_code_parser()

    def _find_java_files(self, root_path: str) -> List[str]:
        """Find all Java files in the given directory and its subdirectories.
        
        Args:
            root_path: Root directory path to search in
            
        Returns:
            List of Java file paths
        """
        java_files = []
        root_path = Path(root_path)
        
        for path in root_path.rglob("*.java"):
            # Skip test files and build directories
            if any(part in path.parts for part in ["test", "build", "target", "bin"]):
                continue
            java_files.append(str(path))
            
        return java_files
    

    def get_separated_code_for_vector(self, root_path: str) -> List[str]:
        """Get the separated code in the codebase for a project.
        
        Args:
            project_name: Name of the project
            
        """
        code_metadata_list = self.java_code_parser.parse_directory(root_path)
        self.logger.info(f"Parsed {len(code_metadata_list)} files in {root_path}")

        result = []
        for code_metadata in code_metadata_list:
            # current strategy is put each file content into the vector
            # TODO: test to put each class content into the vector instead of file content
            # TODO: test to put each method content into the vector instead of file content

            code_vector_metadata = CodeVectorMetadata.from_code_metadata(code_metadata)
            code_data_for_vector = CodeDataForVector(
                transfer_body=code_metadata.content,
                metadata=code_vector_metadata
            )
            result.append(code_data_for_vector)

        return result


    async def update_codebase(
        self,
        project_name: str,
        root_path: str,
        language: Optional[str] = None
    ) -> bool:
        """Update the codebase vectors for a project.
        
        Args:
            project_name: Name of the project
            root_path: Root directory path containing the codebase
            language: Programming language (defaults to settings.DEFAULT_LANGUAGE)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete existing vectors for the project
            self.vector_storage.delete_project_vectors(
                settings.QDRANT_COLLECTION_NAME,
                project_name
            )
            
            language = language or settings.DEFAULT_LANGUAGE
            vectors = []
            vector_metadata_list = []
            
            java_files = self._find_java_files(root_path)
            self.logger.info(f"Found {len(java_files)} Java files in {root_path}")

            separated_codes = self.get_separated_code_for_vector(root_path)

            for separated_code in separated_codes:
                separated_code_vector = await self.vector_embedding.generate_embedding(separated_code.transfer_body)
                vectors.append(separated_code_vector)
                vector_metadata_list.append(separated_code.metadata)

            # Store vectors and metadata
            if vectors and vector_metadata_list:
                success = self.vector_storage.store_vectors(
                    settings.QDRANT_COLLECTION_NAME,
                    vectors,
                    vector_metadata_list
                )
                if not success:
                    self.logger.error("Failed to store vectors")
                    raise Exception("Failed to store vectors")
            
            self.logger.info(f"Stored {len(vectors)} vectors for project {project_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update codebase for project {project_name}: {str(e)}")
            raise e

    async def query_codebase(
        self,
        project_name: str,
        question: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Query the codebase with a natural language question.
        
        Args:
            project_name: Name of the project to query
            question: Natural language question
            limit: Maximum number of results to return
            
        Returns:
            List of relevant code snippets with metadata
        """
        try:
            # Generate vector for the question
            query_vector = await self.vector_embedding.generate_embedding(question)
            
            # Search for similar vectors
            results = self.vector_storage.search_vectors(
                settings.QDRANT_COLLECTION_NAME,
                query_vector,
                limit=limit,
                project_name=project_name
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to query codebase for project {project_name}: {str(e)}")
            return [] 