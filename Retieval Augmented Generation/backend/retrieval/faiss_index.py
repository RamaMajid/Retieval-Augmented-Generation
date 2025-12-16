"""
FAISS Index Manager for vector storage and similarity search.
"""
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import json

from config import settings


class FAISSIndex:
    """
    FAISS vector database manager for efficient similarity search.
    """
    
    def __init__(self, dimension: int = 512, index_type: str = "flat"):
        """
        Initialize FAISS index.
        
        Args:
            dimension: Dimension of embeddings
            index_type: Type of index ("flat", "ivf", "hnsw")
        """
        self.dimension = dimension
        self.index_type = index_type
        self.index = None
        self.metadata = []  # Store metadata for each vector
        
        self._create_index()
    
    def _create_index(self):
        """Create FAISS index based on type."""
        if self.index_type == "flat":
            # Flat index with inner product (for cosine similarity with normalized vectors)
            self.index = faiss.IndexFlatIP(self.dimension)
        elif self.index_type == "ivf":
            # IVF index for faster search on large datasets
            quantizer = faiss.IndexFlatIP(self.dimension)
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, 100)
        elif self.index_type == "hnsw":
            # HNSW index for very fast approximate search
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
        else:
            raise ValueError(f"Unknown index type: {self.index_type}")
        
        print(f"Created FAISS {self.index_type} index with dimension {self.dimension}")
    
    def add_embeddings(
        self, 
        embeddings: np.ndarray, 
        metadata: List[Dict] = None
    ):
        """
        Add embeddings to the index.
        
        Args:
            embeddings: Numpy array of embeddings (shape: [n, dimension])
            metadata: List of metadata dicts for each embedding
        """
        # Ensure embeddings are float32
        embeddings = embeddings.astype(np.float32)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Train index if needed (for IVF)
        if self.index_type == "ivf" and not self.index.is_trained:
            print("Training IVF index...")
            self.index.train(embeddings)
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata
        if metadata:
            self.metadata.extend(metadata)
        else:
            # Create default metadata
            start_idx = len(self.metadata)
            self.metadata.extend([
                {"id": start_idx + i} 
                for i in range(len(embeddings))
            ])
        
        print(f"Added {len(embeddings)} embeddings. Total: {self.index.ntotal}")
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, List[Dict]]:
        """
        Search for similar vectors.
        
        Args:
            query_embedding: Query embedding (shape: [1, dimension] or [dimension])
            k: Number of results to return
            
        Returns:
            Tuple of (distances, indices, metadata)
        """
        # Ensure correct shape
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Ensure float32 and normalize
        query_embedding = query_embedding.astype(np.float32)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Get metadata for results
        result_metadata = [
            self.metadata[idx] if idx < len(self.metadata) else {}
            for idx in indices[0]
        ]
        
        return distances[0], indices[0], result_metadata
    
    def batch_search(
        self, 
        query_embeddings: np.ndarray, 
        k: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, List[List[Dict]]]:
        """
        Search for multiple queries at once.
        
        Args:
            query_embeddings: Query embeddings (shape: [n, dimension])
            k: Number of results per query
            
        Returns:
            Tuple of (distances, indices, metadata_list)
        """
        # Ensure float32 and normalize
        query_embeddings = query_embeddings.astype(np.float32)
        faiss.normalize_L2(query_embeddings)
        
        # Search
        distances, indices = self.index.search(query_embeddings, k)
        
        # Get metadata for all results
        all_metadata = []
        for query_indices in indices:
            result_metadata = [
                self.metadata[idx] if idx < len(self.metadata) else {}
                for idx in query_indices
            ]
            all_metadata.append(result_metadata)
        
        return distances, indices, all_metadata
    
    def save(self, path: str = None):
        """
        Save index and metadata to disk.
        
        Args:
            path: Directory path to save (default from settings)
        """
        path = Path(path or settings.FAISS_INDEX_PATH)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_file = path / "index.faiss"
        faiss.write_index(self.index, str(index_file))
        
        # Save metadata
        metadata_file = path / "metadata.pkl"
        with open(metadata_file, "wb") as f:
            pickle.dump(self.metadata, f)
        
        # Save config
        config_file = path / "config.json"
        config = {
            "dimension": self.dimension,
            "index_type": self.index_type,
            "num_vectors": self.index.ntotal
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"Saved FAISS index to {path}")
    
    def load(self, path: str = None):
        """
        Load index and metadata from disk.
        
        Args:
            path: Directory path to load from (default from settings)
        """
        path = Path(path or settings.FAISS_INDEX_PATH)
        
        # Load FAISS index
        index_file = path / "index.faiss"
        if not index_file.exists():
            raise FileNotFoundError(f"Index file not found: {index_file}")
        
        self.index = faiss.read_index(str(index_file))
        
        # Load metadata
        metadata_file = path / "metadata.pkl"
        if metadata_file.exists():
            with open(metadata_file, "rb") as f:
                self.metadata = pickle.load(f)
        
        # Load config
        config_file = path / "config.json"
        if config_file.exists():
            with open(config_file, "r") as f:
                config = json.load(f)
                self.dimension = config["dimension"]
                self.index_type = config["index_type"]
        
        print(f"Loaded FAISS index from {path}")
        print(f"Total vectors: {self.index.ntotal}")
    
    def clear(self):
        """Clear the index and metadata."""
        self._create_index()
        self.metadata = []
        print("Cleared FAISS index")
    
    def get_stats(self) -> Dict:
        """Get index statistics."""
        return {
            "dimension": self.dimension,
            "index_type": self.index_type,
            "num_vectors": self.index.ntotal,
            "num_metadata": len(self.metadata)
        }
