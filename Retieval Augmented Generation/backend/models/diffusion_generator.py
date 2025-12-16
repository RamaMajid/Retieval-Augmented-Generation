"""
Stable Diffusion Generator for creating new images based on retrieval results.
"""
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
from typing import List, Optional

from config import settings


class DiffusionGenerator:
    """
    Stable Diffusion model wrapper for generating images from text prompts.
    """
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize Stable Diffusion generator.
        
        Args:
            model_name: HuggingFace model name (default from settings)
            device: Device to run model on (default from settings)
        """
        self.model_name = model_name or settings.DIFFUSION_MODEL
        self.device = device or settings.DEVICE
        
        print(f"Loading Stable Diffusion model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load pipeline
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,  # Disable safety checker for faster inference
            requires_safety_checker=False
        )
        
        # Use DPM-Solver for faster generation
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        self.pipe = self.pipe.to(self.device)
        
        # Enable memory optimizations
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
            # Uncomment if you have limited VRAM
            # self.pipe.enable_vae_slicing()
            # self.pipe.enable_sequential_cpu_offload()
        
        print("Stable Diffusion model loaded successfully!")
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "blurry, bad quality, distorted",
        num_inference_steps: int = 25,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None
    ) -> Image.Image:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of desired image
            negative_prompt: What to avoid in the image
            num_inference_steps: Number of denoising steps (more = better quality but slower)
            guidance_scale: How closely to follow the prompt (7-9 is good)
            width: Image width (must be multiple of 8)
            height: Image height (must be multiple of 8)
            seed: Random seed for reproducibility
            
        Returns:
            Generated PIL Image
        """
        # Set seed if provided
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # Generate image
        with torch.no_grad():
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                generator=generator
            )
        
        return result.images[0]
    
    def generate_from_captions(
        self,
        captions: List[str],
        style: str = "photorealistic",
        num_images: int = 1
    ) -> List[Image.Image]:
        """
        Generate images based on retrieved image captions.
        
        Args:
            captions: List of captions from retrieved images
            style: Style modifier (e.g., "photorealistic", "artistic", "cartoon")
            num_images: Number of images to generate
            
        Returns:
            List of generated PIL Images
        """
        # Combine captions into a coherent prompt
        combined_prompt = self._build_prompt_from_captions(captions, style)
        
        images = []
        for i in range(num_images):
            image = self.generate_image(
                prompt=combined_prompt,
                seed=42 + i  # Different seed for each image
            )
            images.append(image)
        
        return images
    
    def _build_prompt_from_captions(
        self, 
        captions: List[str], 
        style: str
    ) -> str:
        """
        Build a Stable Diffusion prompt from image captions.
        
        Args:
            captions: List of image captions
            style: Style modifier
            
        Returns:
            Formatted prompt string
        """
        # Extract key elements from captions
        elements = []
        for caption in captions[:3]:  # Use top 3 captions
            # Simple extraction (can be improved with NLP)
            elements.append(caption)
        
        # Combine elements
        base_prompt = ", ".join(elements)
        
        # Add style modifier
        style_modifiers = {
            "photorealistic": "highly detailed, photorealistic, 8k, professional photography",
            "artistic": "artistic, beautiful, aesthetic, trending on artstation",
            "cartoon": "cartoon style, animated, colorful, vibrant",
            "painting": "oil painting, classical art, museum quality",
            "digital_art": "digital art, concept art, detailed, trending on artstation"
        }
        
        modifier = style_modifiers.get(style, style_modifiers["photorealistic"])
        
        full_prompt = f"{base_prompt}, {modifier}"
        
        return full_prompt
    
    def generate_variations(
        self,
        prompt: str,
        num_variations: int = 4,
        guidance_scale_range: tuple = (7.0, 9.0)
    ) -> List[Image.Image]:
        """
        Generate multiple variations of an image with different parameters.
        
        Args:
            prompt: Text description
            num_variations: Number of variations to generate
            guidance_scale_range: Range of guidance scales to use
            
        Returns:
            List of generated PIL Images
        """
        images = []
        
        for i in range(num_variations):
            # Vary guidance scale
            guidance = guidance_scale_range[0] + (
                (guidance_scale_range[1] - guidance_scale_range[0]) * i / (num_variations - 1)
            )
            
            image = self.generate_image(
                prompt=prompt,
                guidance_scale=guidance,
                seed=42 + i
            )
            images.append(image)
        
        return images
