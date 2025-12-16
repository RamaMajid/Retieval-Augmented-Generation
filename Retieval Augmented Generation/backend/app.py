"""
FastAPI application for Image Retrieval RAG system.
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from pathlib import Path
import shutil
import base64
from io import BytesIO
from PIL import Image

from config import settings
from models import CLIPEncoder, BLIPGenerator, TextGenerator, DiffusionGenerator
from retrieval import SearchEngine
from utils import DatasetLoader
from utils.history_manager import HistoryManager

# Initialize FastAPI app
app = FastAPI(
    title="Image Retrieval RAG API",
    description="Retrieval Augmented Generation system for image search with generative capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (lazy loading)
search_engine: Optional[SearchEngine] = None
diffusion_generator: Optional[DiffusionGenerator] = None
dataset_loader: DatasetLoader = DatasetLoader()


# Pydantic models
class SearchByTextRequest(BaseModel):
    query: str
    k: int = 10
    generate_captions: bool = True
    generate_narrative: bool = True


class GenerateImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = "blurry, bad quality, distorted"
    num_images: int = 1
    style: str = "photorealistic"


class DatasetLoadRequest(BaseModel):
    dataset_name: str  # "fashion_mnist", "cifar10", "custom"
    split: str = "train"
    custom_path: Optional[str] = None


# Helper functions
def get_search_engine():
    """Get or initialize search engine."""
    global search_engine
    if search_engine is None:
        print("Initializing search engine...")
        clip_encoder = CLIPEncoder()
        blip_generator = BLIPGenerator()
        text_generator = TextGenerator()
        search_engine = SearchEngine(
            clip_encoder=clip_encoder,
            blip_generator=blip_generator,
            text_generator=text_generator
        )
        
        # Try to load existing index
        try:
            search_engine.load_index()
            print("Loaded existing FAISS index")
        except FileNotFoundError:
            print("No existing index found. Please load a dataset first.")
    
    return search_engine


def get_diffusion_generator():
    """Get or initialize diffusion generator."""
    global diffusion_generator
    if diffusion_generator is None:
        print("Initializing Stable Diffusion...")
        diffusion_generator = DiffusionGenerator()
    return diffusion_generator


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Image Retrieval RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "search_by_text": "/api/search-by-text",
            "search_by_image": "/api/search-by-image",
            "generate_image": "/api/generate-image",
            "load_dataset": "/api/load-dataset",
            "dataset_info": "/api/dataset-info"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_loaded": search_engine is not None,
        "diffusion_loaded": diffusion_generator is not None
    }


@app.post("/api/search-by-text")
async def search_by_text(request: SearchByTextRequest):
    """
    Search for images using text query.
    """
    try:
        engine = get_search_engine()
        
        # Check if index is loaded
        if engine.faiss_index.index.ntotal == 0:
            raise HTTPException(
                status_code=400,
                detail="No images indexed. Please load a dataset first."
            )
        
        # Perform search with generation
        results = engine.search_with_generation(
            query=request.query,
            k=request.k,
            generate_captions=request.generate_captions,
            generate_narrative=request.generate_narrative
        )
        
        # Auto-save to history
        try:
            history_manager.save_search(
                query=request.query,
                query_type="text",
                results=results.get("results", []),
                narrative=results.get("narrative")
            )
        except Exception as e:
            print(f"Warning: Failed to save to history: {e}")
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search-by-image")
async def search_by_image(
    image: UploadFile = File(...),
    k: int = Form(10),
    generate_captions: bool = Form(True),
    generate_narrative: bool = Form(True)
):
    """
    Search for similar images using an uploaded image.
    """
    try:
        engine = get_search_engine()
        
        # Check if index is loaded
        if engine.faiss_index.index.ntotal == 0:
            raise HTTPException(
                status_code=400,
                detail="No images indexed. Please load a dataset first."
            )
        
        # Read and process uploaded image
        contents = await image.read()
        pil_image = Image.open(BytesIO(contents)).convert("RGB")
        
        # Perform search with generation
        results = engine.search_with_generation(
            query=pil_image,
            k=k,
            generate_captions=generate_captions,
            generate_narrative=generate_narrative
        )
        
        # Auto-save to history
        try:
            history_manager.save_search(
                query=f"Image search: {image.filename}",
                query_type="image",
                results=results.get("results", []),
                narrative=results.get("narrative")
            )
        except Exception as e:
            print(f"Warning: Failed to save to history: {e}")
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-image")
async def generate_image(request: GenerateImageRequest):
    """
    Generate new images using Stable Diffusion.
    """
    try:
        diffusion = get_diffusion_generator()
        
        # Generate images
        images = []
        for i in range(request.num_images):
            img = diffusion.generate_image(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                seed=42 + i
            )
            
            # Convert to base64
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            images.append({
                "index": i,
                "image_base64": img_str
            })
        
        return {
            "prompt": request.prompt,
            "num_images": len(images),
            "images": images
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-from-captions")
async def generate_from_captions(
    captions: List[str],
    style: str = "photorealistic",
    num_images: int = 1
):
    """
    Generate images based on retrieved image captions.
    """
    try:
        diffusion = get_diffusion_generator()
        
        # Generate images
        generated_images = diffusion.generate_from_captions(
            captions=captions,
            style=style,
            num_images=num_images
        )
        
        # Convert to base64
        images = []
        for i, img in enumerate(generated_images):
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            images.append({
                "index": i,
                "image_base64": img_str
            })
        
        return {
            "num_images": len(images),
            "style": style,
            "images": images
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/load-dataset")
async def load_dataset(request: DatasetLoadRequest):
    """
    Load and index a dataset.
    """
    try:
        engine = get_search_engine()
        
        # Load dataset
        if request.dataset_name == "fashion_mnist":
            image_paths = dataset_loader.load_fashion_mnist(split=request.split)
        elif request.dataset_name == "cifar10":
            image_paths = dataset_loader.load_cifar10(split=request.split)
        elif request.dataset_name == "kaggle_fashion":
            image_paths = dataset_loader.load_kaggle_fashion()
        elif request.dataset_name == "custom" and request.custom_path:
            image_paths = dataset_loader.load_custom_dataset(request.custom_path)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown dataset: {request.dataset_name}"
            )
        
        # Index images
        engine.index_images(image_paths, batch_size=32, save_index=True)
        
        return {
            "status": "success",
            "dataset": request.dataset_name,
            "num_images": len(image_paths),
            "indexed": engine.faiss_index.index.ntotal
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dataset-info")
async def get_dataset_info():
    """
    Get information about the current dataset and index.
    """
    try:
        # This will auto-load existing index if available
        engine = get_search_engine()
        
        # Check if index has data
        if engine.faiss_index.index.ntotal == 0:
            return {
                "indexed": False,
                "num_images": 0,
                "message": "No dataset loaded. Please load a dataset first."
            }
        
        stats = engine.get_stats()
        
        return {
            "indexed": True,
            "num_images": stats["faiss_stats"]["num_vectors"],
            "embedding_dim": stats["embedding_dim"],
            "clip_model": stats["clip_model"],
            "has_generation": stats["has_blip"] and stats["has_text_gen"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/image/{image_path:path}")
async def get_image(image_path: str):
    """
    Serve an image file.
    """
    try:
        # Normalize path - convert URL encoded backslashes to forward slashes
        # Windows paths use backslash, but URLs use forward slash
        image_path = image_path.replace("%5C", "/").replace("\\", "/")
        
        # Convert to Path object and resolve
        file_path = Path(image_path)
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"Image not found: {image_path}"
            )
        
        return FileResponse(file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Search History Endpoints
# ============================================================================

# Initialize history manager
history_manager = HistoryManager()


@app.get("/api/history/list")
async def get_history_list(
    limit: Optional[int] = 50,
    offset: int = 0,
    favorites_only: bool = False
):
    """
    Get list of search history.
    
    Args:
        limit: Maximum number of entries to return
        offset: Number of entries to skip (for pagination)
        favorites_only: Only return favorited searches
    """
    try:
        searches = history_manager.get_all(
            limit=limit,
            offset=offset,
            favorites_only=favorites_only
        )
        
        return {
            "searches": searches,
            "count": len(searches),
            "offset": offset,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{search_id}")
async def get_history_item(search_id: str):
    """
    Get a specific search from history by ID.
    """
    try:
        search = history_manager.get_by_id(search_id)
        
        if search is None:
            raise HTTPException(status_code=404, detail="Search not found")
        
        return search
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/history/{search_id}")
async def delete_history_item(search_id: str):
    """
    Delete a specific search from history.
    """
    try:
        success = history_manager.delete(search_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Search not found")
        
        return {"message": "Search deleted successfully", "id": search_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/history/clear/all")
async def clear_all_history():
    """
    Clear all search history.
    """
    try:
        count = history_manager.clear_all()
        
        return {
            "message": "All history cleared",
            "deleted_count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/history/{search_id}/favorite")
async def toggle_favorite(search_id: str):
    """
    Toggle favorite status of a search.
    """
    try:
        new_status = history_manager.toggle_favorite(search_id)
        
        if new_status is None:
            raise HTTPException(status_code=404, detail="Search not found")
        
        return {
            "id": search_id,
            "is_favorite": new_status,
            "message": "Favorite status updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/export/all")
async def export_history():
    """
    Export all search history as JSON.
    """
    try:
        data = history_manager.export_all()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/stats")
async def get_history_stats():
    """
    Get statistics about search history.
    """
    try:
        stats = history_manager.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False
    )
