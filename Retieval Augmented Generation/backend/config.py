"""
Configuration management for the Image Retrieval RAG system.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Paths
    MODEL_CACHE_DIR: str = "./models_cache"
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    DATASET_PATH: str = "./data/dataset"
    
    # Device
    DEVICE: str = "cuda" if os.environ.get("DEVICE", "cpu") == "cuda" else "cpu"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Model Names
    CLIP_MODEL: str = "openai/clip-vit-base-patch32"
    BLIP_MODEL: str = "Salesforce/blip2-opt-2.7b"
    TEXT_GEN_MODEL: str = "google/flan-t5-base"
    DIFFUSION_MODEL: str = "stabilityai/stable-diffusion-2-1"
    
    # Generation Parameters
    MAX_CAPTION_LENGTH: int = 50
    MAX_NARRATIVE_LENGTH: int = 200
    TOP_K_RESULTS: int = 10
    
    # Optional OpenAI
    OPENAI_API_KEY: str | None = None
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS from comma-separated string."""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Ensure directories exist
Path(settings.MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.FAISS_INDEX_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(settings.DATASET_PATH).mkdir(parents=True, exist_ok=True)
