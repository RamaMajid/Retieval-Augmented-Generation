"""
CLIP Encoder for generating image and text embeddings.
"""
import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import Union, List
from pathlib import Path

from config import settings


class CLIPEncoder:
    """
    CLIP model wrapper for encoding images and text into embeddings.
    """
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize CLIP encoder.
        
        Args:
            model_name: HuggingFace model name (default from settings)
            device: Device to run model on (default from settings)
        """
        self.model_name = model_name or settings.CLIP_MODEL
        self.device = device or settings.DEVICE
        
        print(f"Loading CLIP model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load model and processor
        self.model = CLIPModel.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR
        ).to(self.device)
        
        self.processor = CLIPProcessor.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR
        )
        
        self.model.eval()
        print("CLIP model loaded successfully!")
    
    def encode_image(
        self, 
        image: Union[Image.Image, str, Path, List[Union[Image.Image, str, Path]]]
    ) -> np.ndarray:
        """
        Encode image(s) into embeddings.
        
        Args:
            image: Single image or list of images (PIL Image, path, or file path)
            
        Returns:
            Normalized embeddings as numpy array (shape: [n, embedding_dim])
        """
        # Handle single image
        if not isinstance(image, list):
            image = [image]
        
        # Load images if paths are provided
        images = []
        for img in image:
            if isinstance(img, (str, Path)):
                images.append(Image.open(img).convert("RGB"))
            else:
                images.append(img.convert("RGB") if img.mode != "RGB" else img)
        
        # Process images
        inputs = self.processor(
            images=images,
            return_tensors="pt",
            padding=True
        ).to(self.device)
        
        # Generate embeddings
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            
        # Normalize embeddings
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy()
    
    def encode_text(
        self, 
        text: Union[str, List[str]]
    ) -> np.ndarray:
        """
        Encode text(s) into embeddings.
        
        Args:
            text: Single text or list of texts
            
        Returns:
            Normalized embeddings as numpy array (shape: [n, embedding_dim])
        """
        # Handle single text
        if isinstance(text, str):
            text = [text]
        
        # Process text
        inputs = self.processor(
            text=text,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)
        
        # Generate embeddings
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        
        # Normalize embeddings
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        return text_features.cpu().numpy()
    
    def get_embedding_dim(self) -> int:
        """Get the dimension of embeddings."""
        return self.model.config.projection_dim
    
    def compute_similarity(
        self, 
        embeddings1: np.ndarray, 
        embeddings2: np.ndarray
    ) -> np.ndarray:
        """
        Compute cosine similarity between two sets of embeddings.
        
        Args:
            embeddings1: First set of embeddings (shape: [n, dim])
            embeddings2: Second set of embeddings (shape: [m, dim])
            
        Returns:
            Similarity matrix (shape: [n, m])
        """
        # Embeddings are already normalized, so dot product = cosine similarity
        return np.dot(embeddings1, embeddings2.T)
