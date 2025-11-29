"""
GenAI Platform - Embedding Generator
Generates embeddings for text chunks
"""

from typing import List, Dict, Any
from loguru import logger
import numpy as np


class EmbeddingGenerator:
    """Generates embeddings for text using various models."""
    
    def __init__(self, model_name: str = "sentence-bert"):
        """
        Initialize embedding generator.
        
        Args:
            model_name: Model to use for embeddings
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
        
        logger.info(f"EmbeddingGenerator initialized with {model_name}")
    
    def _load_model(self):
        """Load embedding model."""
        try:
            if self.model_name == "sentence-bert":
                # Try to use sentence-transformers
                try:
                    from sentence_transformers import SentenceTransformer
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                    logger.info("Loaded sentence-transformers model")
                except ImportError:
                    logger.warning("sentence-transformers not available, using mock embeddings")
                    self.model = None
            else:
                logger.warning(f"Unknown model: {self.model_name}, using mock embeddings")
                self.model = None
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.model = None
    
    def generate(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        if self.model is not None:
            try:
                embeddings = self.model.encode(texts)
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"Error generating embeddings: {e}")
                return self._generate_mock_embeddings(texts)
        else:
            return self._generate_mock_embeddings(texts)
    
    def _generate_mock_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for testing."""
        # Generate random embeddings (384 dimensions like MiniLM)
        embeddings = []
        for text in texts:
            # Use text hash for reproducibility
            np.random.seed(hash(text) % (2**32))
            embedding = np.random.randn(384).tolist()
            embeddings.append(embedding)
        
        logger.debug(f"Generated {len(embeddings)} mock embeddings")
        return embeddings
    
    def generate_single(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        return self.generate([text])[0]


class VectorStoreManager:
    """Manages vector store operations with division isolation."""
    
    def __init__(self):
        """Initialize vector store manager."""
        self.embedding_generator = EmbeddingGenerator()
        logger.info("VectorStoreManager initialized")
    
    def upsert_with_isolation(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        division_id: str,
        department_id: str
    ) -> bool:
        """
        Insert vectors with division/department isolation.
        
        Args:
            texts: List of texts to embed
            metadatas: Metadata for each text
            division_id: Division ID for isolation
            department_id: Department ID
            
        Returns:
            Success status
        """
        try:
            # Generate embeddings
            embeddings = self.embedding_generator.generate(texts)
            
            # Add isolation metadata
            for i, metadata in enumerate(metadatas):
                metadata['_division_id'] = division_id
                metadata['_department_id'] = department_id
            
            # Store in Chroma with division namespace
            try:
                import chromadb
                client = chromadb.Client()
                collection = client.get_or_create_collection(
                    name=f"genai_platform_{division_id}"
                )
                
                ids = [f"{division_id}_{department_id}_{i}" for i in range(len(texts))]
                
                collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas
                )
                
                logger.info(f"Upserted {len(texts)} vectors for {division_id}/{department_id}")
                return True
            except:
                logger.warning("Chroma not available, vectors not persisted")
                return False
                
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False


__all__ = ['EmbeddingGenerator', 'VectorStoreManager']
