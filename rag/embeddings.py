import os
import sys
import traceback
from typing import List
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv(override=True)


class EmbeddingService:
    """Service for generating embeddings using HuggingFace sentence-transformers"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.model = None
        # Use a local cache directory to avoid permission issues
        self.cache_folder = os.path.join(os.getcwd(), "model_cache")
        os.makedirs(self.cache_folder, exist_ok=True)
    
    def _load_model(self):
        """Load the sentence transformer model if not already loaded"""
        if self.model is None:
            try:
                print(f"Loading embedding model: {self.model_name}...")
                print(f"Cache folder: {self.cache_folder}")
                
                # Force download/load from local cache
                self.model = SentenceTransformer(self.model_name, cache_folder=self.cache_folder)
                print("Embedding model loaded successfully.")
            except Exception as e:
                print(f"Error loading embedding model: {e}")
                traceback.print_exc()
                raise RuntimeError(f"Failed to load embedding model: {e}")
    
    def encode(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        self._load_model()
        
        if not self.model:
            raise RuntimeError("Embedding model not loaded")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        self._load_model()
        
        if not self.model:
            raise RuntimeError("Embedding model not loaded")
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    @property
    def dimension(self) -> int:
        """Get the embedding dimension"""
        self._load_model()
        return self.model.get_sentence_embedding_dimension()


# Global instance
embedding_service = EmbeddingService()
