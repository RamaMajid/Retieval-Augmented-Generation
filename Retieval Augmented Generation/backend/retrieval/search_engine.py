"""
High-level search engine combining CLIP encoding and FAISS retrieval.
"""
import numpy as np
from PIL import Image
from typing import Union, List, Dict, Tuple
from pathlib import Path

from models import CLIPEncoder, BLIPGenerator, TextGenerator
from retrieval.faiss_index import FAISSIndex
from config import settings


class SearchEngine:
    """
    High-level search engine for image retrieval with generative capabilities.
    """
    
    def __init__(
        self,
        clip_encoder: CLIPEncoder = None,
        faiss_index: FAISSIndex = None,
        blip_generator: BLIPGenerator = None,
        text_generator: TextGenerator = None
    ):
        """
        Initialize search engine.
        
        Args:
            clip_encoder: CLIP encoder instance (creates new if None)
            faiss_index: FAISS index instance (creates new if None)
            blip_generator: BLIP generator instance (optional)
            text_generator: Text generator instance (optional)
        """
        self.clip_encoder = clip_encoder or CLIPEncoder()
        self.faiss_index = faiss_index or FAISSIndex(
            dimension=self.clip_encoder.get_embedding_dim()
        )
        self.blip_generator = blip_generator
        self.text_generator = text_generator
    
    def search_by_image(
        self,
        image: Union[Image.Image, str, Path],
        k: int = None,
        return_scores: bool = True
    ) -> List[Dict]:
        """
        Search for similar images using an image query.
        
        Args:
            image: Query image (PIL Image or path)
            k: Number of results (default from settings)
            return_scores: Whether to include similarity scores
            
        Returns:
            List of result dictionaries with metadata and scores
        """
        k = k or settings.TOP_K_RESULTS
        
        # Encode query image
        query_embedding = self.clip_encoder.encode_image(image)
        
        # Search in FAISS
        distances, indices, metadata = self.faiss_index.search(
            query_embedding, k=k
        )
        
        # Format results
        results = []
        for i, (dist, idx, meta) in enumerate(zip(distances, indices, metadata)):
            result = {
                "rank": i + 1,
                "index": int(idx),
                "similarity": float(dist),
                **meta
            }
            results.append(result)
        
        return results
    
    def search_by_text(
        self,
        text: str,
        k: int = None,
        return_scores: bool = True
    ) -> List[Dict]:
        """
        Search for images using a text query.
        
        Args:
            text: Query text
            k: Number of results (default from settings)
            return_scores: Whether to include similarity scores
            
        Returns:
            List of result dictionaries with metadata and scores
        """
        k = k or settings.TOP_K_RESULTS
        
        # Encode query text
        query_embedding = self.clip_encoder.encode_text(text)
        
        # Search in FAISS
        distances, indices, metadata = self.faiss_index.search(
            query_embedding, k=k
        )
        
        # Format results
        results = []
        for i, (dist, idx, meta) in enumerate(zip(distances, indices, metadata)):
            result = {
                "rank": i + 1,
                "index": int(idx),
                "similarity": float(dist),
                **meta
            }
            results.append(result)
        
        return results
    
    def search_with_generation(
        self,
        query: Union[str, Image.Image, Path],
        k: int = None,
        generate_captions: bool = True,
        generate_narrative: bool = True
    ) -> Dict:
        """
        Search and generate captions/narrative for results.
        
        Args:
            query: Text query or image
            k: Number of results
            generate_captions: Whether to generate captions
            generate_narrative: Whether to generate narrative
            
        Returns:
            Dictionary with results, captions, and narrative
        """
        k = k or settings.TOP_K_RESULTS
        
        # Determine query type and search
        if isinstance(query, str):
            results = self.search_by_text(query, k=k)
            query_text = query
        else:
            results = self.search_by_image(query, k=k)
            query_text = None
        
        response = {
            "results": results,
            "query_type": "text" if isinstance(query, str) else "image"
        }
        
        # Generate captions if requested
        if generate_captions and self.blip_generator:
            captions = []
            for result in results:
                if "image_path" in result:
                    try:
                        caption = self.blip_generator.generate_caption(
                            result["image_path"]
                        )
                        captions.append(caption)
                    except Exception as e:
                        print(f"Error generating caption: {e}")
                        captions.append("")
                else:
                    captions.append("")
            
            response["captions"] = captions
            
            # Add captions to results
            for result, caption in zip(results, captions):
                result["caption"] = caption
        
        # Generate narrative if requested
        if generate_narrative and self.text_generator and "captions" in response:
            try:
                narrative = self.text_generator.generate_narrative(
                    captions=response["captions"],
                    query=query_text
                )
                response["narrative"] = narrative
            except Exception as e:
                print(f"Error generating narrative: {e}")
                response["narrative"] = ""
        
        return response
    
    def index_images(
        self,
        image_paths: List[str],
        batch_size: int = 32,
        save_index: bool = True
    ):
        """
        Index a list of images.
        
        Args:
            image_paths: List of image file paths
            batch_size: Batch size for encoding
            save_index: Whether to save index after indexing
        """
        from tqdm import tqdm
        
        print(f"Indexing {len(image_paths)} images...")
        
        # Process in batches
        for i in tqdm(range(0, len(image_paths), batch_size)):
            batch_paths = image_paths[i:i + batch_size]
            
            # Load and encode images
            try:
                embeddings = self.clip_encoder.encode_image(batch_paths)
                
                # Create metadata
                metadata = [
                    {
                        "image_path": str(path).replace("\\", "/"),  # Convert to forward slashes for URLs
                        "filename": Path(path).name
                    }
                    for path in batch_paths
                ]
                
                # Add to index
                self.faiss_index.add_embeddings(embeddings, metadata)
                
            except Exception as e:
                print(f"Error processing batch {i}: {e}")
                continue
        
        print(f"Indexing complete! Total vectors: {self.faiss_index.index.ntotal}")
        
        # Save index
        if save_index:
            self.faiss_index.save()
    
    def load_index(self, path: str = None):
        """Load FAISS index from disk."""
        self.faiss_index.load(path)
    
    def save_index(self, path: str = None):
        """Save FAISS index to disk."""
        self.faiss_index.save(path)
    
    def get_stats(self) -> Dict:
        """Get search engine statistics."""
        return {
            "faiss_stats": self.faiss_index.get_stats(),
            "clip_model": self.clip_encoder.model_name,
            "embedding_dim": self.clip_encoder.get_embedding_dim(),
            "has_blip": self.blip_generator is not None,
            "has_text_gen": self.text_generator is not None
        }
