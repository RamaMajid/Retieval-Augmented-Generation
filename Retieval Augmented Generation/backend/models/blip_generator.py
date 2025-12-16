"""
BLIP-2 Generator for image captioning.
"""
import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from typing import Union, List
from pathlib import Path

from config import settings


class BLIPGenerator:
    """
    BLIP-2 model wrapper for generating image captions.
    """
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize BLIP-2 generator.
        
        Args:
            model_name: HuggingFace model name (default from settings)
            device: Device to run model on (default from settings)
        """
        self.model_name = model_name or settings.BLIP_MODEL
        self.device = device or settings.DEVICE
        
        print(f"Loading BLIP-2 model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load model and processor
        self.processor = Blip2Processor.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR
        )
        
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        
        self.model.eval()
        print("BLIP-2 model loaded successfully!")
    
    def generate_caption(
        self,
        image: Union[Image.Image, str, Path],
        prompt: str = "a photo of",
        max_length: int = None,
        num_beams: int = 5,
        temperature: float = 1.0
    ) -> str:
        """
        Generate caption for a single image.
        
        Args:
            image: PIL Image or path to image
            prompt: Optional prompt to guide generation
            max_length: Maximum caption length (default from settings)
            num_beams: Number of beams for beam search
            temperature: Sampling temperature
            
        Returns:
            Generated caption as string
        """
        # Load image if path is provided
        if isinstance(image, (str, Path)):
            image = Image.open(image).convert("RGB")
        else:
            image = image.convert("RGB") if image.mode != "RGB" else image
        
        max_length = max_length or settings.MAX_CAPTION_LENGTH
        
        # Process image
        inputs = self.processor(
            images=image,
            text=prompt,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate caption
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                temperature=temperature,
                do_sample=False
            )
        
        # Decode caption
        caption = self.processor.batch_decode(
            generated_ids, 
            skip_special_tokens=True
        )[0].strip()
        
        return caption
    
    def generate_batch_captions(
        self,
        images: List[Union[Image.Image, str, Path]],
        prompt: str = "a photo of",
        max_length: int = None,
        num_beams: int = 5,
        temperature: float = 1.0
    ) -> List[str]:
        """
        Generate captions for multiple images.
        
        Args:
            images: List of PIL Images or paths
            prompt: Optional prompt to guide generation
            max_length: Maximum caption length (default from settings)
            num_beams: Number of beams for beam search
            temperature: Sampling temperature
            
        Returns:
            List of generated captions
        """
        captions = []
        
        # Process images one by one to avoid memory issues
        for image in images:
            caption = self.generate_caption(
                image=image,
                prompt=prompt,
                max_length=max_length,
                num_beams=num_beams,
                temperature=temperature
            )
            captions.append(caption)
        
        return captions
    
    def generate_detailed_caption(
        self,
        image: Union[Image.Image, str, Path],
        max_length: int = 100
    ) -> str:
        """
        Generate a more detailed caption for an image.
        
        Args:
            image: PIL Image or path to image
            max_length: Maximum caption length
            
        Returns:
            Detailed caption as string
        """
        return self.generate_caption(
            image=image,
            prompt="Describe this image in detail:",
            max_length=max_length,
            num_beams=8,
            temperature=0.9
        )
