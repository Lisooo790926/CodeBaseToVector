import os
from typing import List
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config.settings import settings

class VectorEmbeddingService:
    """Service for generating embeddings using Google Generative AI.
    
    This class handles the integration with Google's Generative AI for generating
    text embeddings from code snippets and related metadata.
    """
    
    def __init__(self):
        """Initialize the embedding service with Google Generative AI."""
        self.logger = logging.getLogger(__name__)
        try:
            self.logger.debug("Initializing Google Generative AI embedding service...")
            self.model = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-exp-03-07",
                google_api_key=settings.GOOGLE_API_KEY,
                task_type="retrieval_document",
            )
            self.logger.info("Successfully initialized Google Generative AI embedding service")
        except Exception as e:
            self.logger.error(f"Failed to initialize embedding service: {str(e)}")
            raise

    def _preprocess_code(self, code: str) -> str:
        """Preprocess code snippet for embedding generation.
        
        This function performs the following preprocessing steps:
        1. Removes empty lines
        2. Preserves indentation but removes extra whitespace
        3. Joins the lines back together
        
        Args:
            code: Raw code snippet
            
        Returns:
            Preprocessed code ready for embedding
        """
        self.logger.debug(f"Starting code preprocessing. Original length: {len(code.split(chr(10)))}")
        
        # 移除空白行但保留縮進
        lines = code.split('\n')
        processed_lines = []
        for line in lines:
            if line.strip():  # 如果行不是完全空白
                # 保留前導空格，但移除其他多餘空格
                indent = len(line) - len(line.lstrip())
                processed_line = line[:indent] + ' '.join(line[indent:].split())
                processed_lines.append(processed_line)
        
        processed_code = '\n'.join(processed_lines)
        self.logger.debug(f"Finished preprocessing. Final length: {len(processed_code.split(chr(10)))}")
        return processed_code

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text snippet.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List of embedding values
        """
        try:
            self.logger.debug(f"Generating embedding for text of length: {len(text)}")
            processed_text = self._preprocess_code(text)
            
            embedding = await self.model.aembed_query(processed_text)
            self.logger.debug(f"Generated embedding of dimension: {len(embedding)}")
            
            return embedding
            
        except Exception as e:
            self.logger.error(f"Error generating embedding: {str(e)}")
            raise

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embedding vectors
        """
        try:
            self.logger.debug(f"Processing batch of {len(texts)} texts")
            processed_texts = [self._preprocess_code(text) for text in texts]
            
            embeddings = await self.model.aembed_documents(processed_texts)
            self.logger.info(f"Generated {len(embeddings)} embeddings")
            
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error generating batch embeddings: {str(e)}")
            raise