"""
Example script to initialize and test the Image Retrieval RAG system.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from models import CLIPEncoder, BLIPGenerator, TextGenerator, DiffusionGenerator
from retrieval import SearchEngine
from utils import DatasetLoader
from config import settings


def main():
    print("=" * 60)
    print("Image Retrieval RAG System - Initialization")
    print("=" * 60)
    
    # 1. Initialize models
    print("\n[1/5] Initializing CLIP encoder...")
    clip_encoder = CLIPEncoder()
    
    print("\n[2/5] Initializing BLIP-2 generator...")
    blip_generator = BLIPGenerator()
    
    print("\n[3/5] Initializing text generator...")
    text_generator = TextGenerator()
    
    print("\n[4/5] Initializing search engine...")
    search_engine = SearchEngine(
        clip_encoder=clip_encoder,
        blip_generator=blip_generator,
        text_generator=text_generator
    )
    
    # 2. Load dataset
    print("\n[5/5] Loading dataset...")
    dataset_loader = DatasetLoader()
    
    # Load Fashion-MNIST (you can change this to other datasets)
    print("Loading Fashion-MNIST dataset...")
    image_paths = dataset_loader.load_fashion_mnist(split="train")
    
    print(f"Loaded {len(image_paths)} images")
    
    # 3. Index images
    print("\nIndexing images (this may take a while)...")
    search_engine.index_images(
        image_paths=image_paths[:1000],  # Index first 1000 images for testing
        batch_size=32,
        save_index=True
    )
    
    print("\n" + "=" * 60)
    print("Initialization Complete!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Start the backend server: python app.py")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Open http://localhost:3000 in your browser")
    print("\nOr test the search engine directly:")
    
    # 4. Test search
    print("\n" + "=" * 60)
    print("Testing Search Engine")
    print("=" * 60)
    
    test_query = "sneakers"
    print(f"\nSearching for: '{test_query}'")
    
    results = search_engine.search_with_generation(
        query=test_query,
        k=5,
        generate_captions=True,
        generate_narrative=True
    )
    
    print(f"\nFound {len(results['results'])} results:")
    for i, result in enumerate(results['results'][:3], 1):
        print(f"\n{i}. Similarity: {result['similarity']:.3f}")
        print(f"   File: {result['filename']}")
        if 'caption' in result:
            print(f"   Caption: {result['caption']}")
    
    if 'narrative' in results:
        print(f"\nGenerated Narrative:")
        print(f"{results['narrative']}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
