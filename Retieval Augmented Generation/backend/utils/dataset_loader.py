"""
Dataset loader for various image datasets.
"""
import os
import numpy as np
from PIL import Image
from pathlib import Path
from typing import List, Tuple, Optional
import torchvision
import torchvision.transforms as transforms
from tqdm import tqdm

from config import settings


class DatasetLoader:
    """
    Utility class for loading and processing various image datasets.
    """
    
    def __init__(self, dataset_path: str = None):
        """
        Initialize dataset loader.
        
        Args:
            dataset_path: Path to save/load datasets (default from settings)
        """
        self.dataset_path = Path(dataset_path or settings.DATASET_PATH)
        self.dataset_path.mkdir(parents=True, exist_ok=True)
    
    def load_fashion_mnist(
        self,
        split: str = "train",
        save_images: bool = True
    ) -> List[str]:
        """
        Load Fashion-MNIST dataset and save as images.
        
        Args:
            split: "train" or "test"
            save_images: Whether to save images to disk
            
        Returns:
            List of image paths
        """
        print(f"Loading Fashion-MNIST ({split} split)...")
        
        # Download dataset
        is_train = (split == "train")
        dataset = torchvision.datasets.FashionMNIST(
            root=str(self.dataset_path / "fashion_mnist_raw"),
            train=is_train,
            download=True
        )
        
        # Create output directory
        output_dir = self.dataset_path / f"fashion_mnist_{split}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        image_paths = []
        
        if save_images:
            print(f"Saving {len(dataset)} images...")
            for idx, (img, label) in enumerate(tqdm(dataset)):
                # Convert to RGB
                img_rgb = img.convert("RGB")
                
                # Save image
                img_path = output_dir / f"{idx:05d}_class{label}.png"
                img_rgb.save(img_path)
                image_paths.append(str(img_path))
        else:
            # Just return paths without saving
            for idx, (img, label) in enumerate(dataset):
                img_path = output_dir / f"{idx:05d}_class{label}.png"
                image_paths.append(str(img_path))
        
        print(f"Loaded {len(image_paths)} images from Fashion-MNIST")
        return image_paths
    
    def load_cifar10(
        self,
        split: str = "train",
        save_images: bool = True
    ) -> List[str]:
        """
        Load CIFAR-10 dataset and save as images.
        
        Args:
            split: "train" or "test"
            save_images: Whether to save images to disk
            
        Returns:
            List of image paths
        """
        print(f"Loading CIFAR-10 ({split} split)...")
        
        # Download dataset
        is_train = (split == "train")
        dataset = torchvision.datasets.CIFAR10(
            root=str(self.dataset_path / "cifar10_raw"),
            train=is_train,
            download=True
        )
        
        # Create output directory
        output_dir = self.dataset_path / f"cifar10_{split}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        image_paths = []
        
        if save_images:
            print(f"Saving {len(dataset)} images...")
            for idx, (img, label) in enumerate(tqdm(dataset)):
                # Save image
                img_path = output_dir / f"{idx:05d}_class{label}.png"
                img.save(img_path)
                image_paths.append(str(img_path))
        else:
            # Just return paths without saving
            for idx, (img, label) in enumerate(dataset):
                img_path = output_dir / f"{idx:05d}_class{label}.png"
                image_paths.append(str(img_path))
        
        print(f"Loaded {len(image_paths)} images from CIFAR-10")
        return image_paths
    
    def load_custom_dataset(
        self,
        dataset_dir: str,
        extensions: List[str] = None
    ) -> List[str]:
        """
        Load custom dataset from a directory.
        
        Args:
            dataset_dir: Directory containing images
            extensions: List of valid image extensions
            
        Returns:
            List of image paths
        """
        if extensions is None:
            extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
        
        dataset_dir = Path(dataset_dir)
        
        print(f"Loading custom dataset from {dataset_dir}...")
        
        image_paths = []
        for ext in extensions:
            image_paths.extend([
                str(p) for p in dataset_dir.rglob(f"*{ext}")
            ])
        
        print(f"Found {len(image_paths)} images")
        return sorted(image_paths)
    
    def load_kaggle_fashion(
        self,
        dataset_dir: str = None,
        max_images: int = None,
        categories: List[str] = None
    ) -> List[str]:
        """
        Load Kaggle Fashion Product dataset.
        
        Args:
            dataset_dir: Path to kaggle fashion dataset (default: data/kaggle_fashion)
            max_images: Maximum number of images to load
            categories: Filter by specific categories (e.g., ['Topwear', 'Shoes'])
            
        Returns:
            List of image paths
        """
        import pandas as pd
        
        if dataset_dir is None:
            # Try to find kaggle_fashion in the correct location
            # First try: data/kaggle_fashion (if dataset_path is 'data/dataset')
            dataset_dir = Path(self.dataset_path).parent / "kaggle_fashion"
            # If not found, try: data/dataset/kaggle_fashion
            if not dataset_dir.exists():
                dataset_dir = self.dataset_path / "kaggle_fashion"
        else:
            dataset_dir = Path(dataset_dir)
        
        print(f"Loading Kaggle Fashion Product dataset from {dataset_dir}...")
        
        # Check if dataset exists
        if not dataset_dir.exists():
            raise FileNotFoundError(
                f"Dataset not found at {dataset_dir}. "
                f"Please download from: https://www.kaggle.com/datasets/nirmalsankalana/fashion-product-text-images-dataset"
            )
        
        # Look for CSV metadata
        csv_file = None
        for csv_name in ["styles.csv", "metadata.csv", "data.csv"]:
            potential_csv = dataset_dir / csv_name
            if potential_csv.exists():
                csv_file = potential_csv
                break
        
        images_dir = dataset_dir / "images"
        
        # If CSV exists, use it for metadata
        if csv_file and csv_file.exists():
            print(f"Found metadata file: {csv_file.name}")
            try:
                df = pd.read_csv(csv_file)
                print(f"Loaded {len(df)} entries from CSV")
                
                # Filter by categories if specified
                if categories and 'masterCategory' in df.columns:
                    df = df[df['masterCategory'].isin(categories)]
                    print(f"Filtered to {len(df)} entries in categories: {categories}")
                
                # Get image paths from CSV
                image_paths = []
                print(f"Searching for images in directories:")
                print(f"  - {images_dir}")
                print(f"  - {dataset_dir / 'data'}")
                print(f"  - {dataset_dir}")
                
                for idx, row in df.iterrows():
                    # Try different column names for image ID/filename
                    img_id = None
                    for col in ['id', 'image_id', 'filename', 'image']:
                        if col in row and pd.notna(row[col]):
                            img_id = str(row[col]).strip()
                            break
                    
                    if img_id:
                        # Try different locations and extensions
                        found = False
                        for subdir in [images_dir, dataset_dir / "data", dataset_dir]:
                            if found:
                                break
                            for ext in ['', '.jpg', '.jpeg', '.png']:
                                # If img_id already has extension, don't add another
                                if '.' in img_id and ext:
                                    continue
                                img_path = subdir / f"{img_id}{ext}"
                                if img_path.exists():
                                    image_paths.append(str(img_path))
                                    found = True
                                    break
                    
                    # Debug: print first few attempts
                    if idx < 3:
                        print(f"Row {idx}: img_id='{img_id}', found={found}")
                    
                    # Stop if we've reached max_images
                    if max_images and len(image_paths) >= max_images:
                        break
                
                print(f"Found {len(image_paths)} valid images from CSV")
                
            except Exception as e:
                print(f"Error reading CSV: {e}")
                print("Falling back to directory scan...")
                image_paths = self._scan_image_directory(images_dir, max_images)
        else:
            # No CSV, just scan directory
            print("No metadata CSV found, scanning images directory...")
            image_paths = self._scan_image_directory(images_dir, max_images)
        
        if not image_paths:
            raise ValueError(
                f"No images found in {dataset_dir}. "
                f"Please check the dataset structure."
            )
        
        print(f"Loaded {len(image_paths)} images from Kaggle Fashion dataset")
        return image_paths
    
    def _scan_image_directory(
        self,
        images_dir: Path,
        max_images: int = None
    ) -> List[str]:
        """Helper method to scan directory for images."""
        if not images_dir.exists():
            return []
        
        extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
        image_paths = []
        
        for ext in extensions:
            found = list(images_dir.glob(f"*{ext}"))
            image_paths.extend([str(p) for p in found])
            
            if max_images and len(image_paths) >= max_images:
                break
        
        if max_images:
            image_paths = image_paths[:max_images]
        
        return sorted(image_paths)
    
    def load_coco_captions(
        self,
        split: str = "train",
        year: str = "2017",
        max_images: int = None
    ) -> Tuple[List[str], List[str]]:
        """
        Load COCO Captions dataset.
        
        Args:
            split: "train" or "val"
            year: Dataset year ("2014" or "2017")
            max_images: Maximum number of images to load
            
        Returns:
            Tuple of (image_paths, captions)
        """
        print(f"Loading COCO Captions ({split} {year})...")
        
        try:
            from pycocotools.coco import COCO
        except ImportError:
            print("pycocotools not installed. Install with: pip install pycocotools")
            return [], []
        
        # Download dataset
        dataset = torchvision.datasets.CocoCaptions(
            root=str(self.dataset_path / f"coco_{year}_{split}"),
            annFile=str(self.dataset_path / f"coco_{year}_{split}" / "annotations" / f"captions_{split}{year}.json"),
            download=True
        )
        
        image_paths = []
        captions = []
        
        limit = max_images or len(dataset)
        for idx in tqdm(range(min(limit, len(dataset)))):
            img, caps = dataset[idx]
            
            # Save image
            img_path = self.dataset_path / f"coco_{year}_{split}" / f"{idx:06d}.jpg"
            if not img_path.exists():
                img.save(img_path)
            
            image_paths.append(str(img_path))
            # Use first caption
            captions.append(caps[0] if caps else "")
        
        print(f"Loaded {len(image_paths)} images from COCO")
        return image_paths, captions
    
    def preprocess_images(
        self,
        image_paths: List[str],
        output_dir: str,
        size: Tuple[int, int] = (224, 224),
        quality: int = 95
    ) -> List[str]:
        """
        Preprocess images (resize, normalize, etc.).
        
        Args:
            image_paths: List of input image paths
            output_dir: Directory to save processed images
            size: Target size (width, height)
            quality: JPEG quality (1-100)
            
        Returns:
            List of processed image paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Preprocessing {len(image_paths)} images...")
        
        processed_paths = []
        
        for img_path in tqdm(image_paths):
            try:
                # Load image
                img = Image.open(img_path).convert("RGB")
                
                # Resize
                img_resized = img.resize(size, Image.Resampling.LANCZOS)
                
                # Save
                output_path = output_dir / Path(img_path).name
                img_resized.save(output_path, quality=quality)
                
                processed_paths.append(str(output_path))
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                continue
        
        print(f"Processed {len(processed_paths)} images")
        return processed_paths
    
    def get_dataset_info(self, dataset_name: str) -> dict:
        """
        Get information about available datasets.
        
        Args:
            dataset_name: Name of dataset
            
        Returns:
            Dictionary with dataset information
        """
        datasets_info = {
            "fashion_mnist": {
                "name": "Fashion-MNIST",
                "num_classes": 10,
                "image_size": (28, 28),
                "num_train": 60000,
                "num_test": 10000,
                "description": "Fashion items (clothing, shoes, bags)"
            },
            "cifar10": {
                "name": "CIFAR-10",
                "num_classes": 10,
                "image_size": (32, 32),
                "num_train": 50000,
                "num_test": 10000,
                "description": "Common objects (airplane, car, bird, cat, etc.)"
            },
            "coco": {
                "name": "COCO Captions",
                "num_classes": 80,
                "image_size": "variable",
                "num_train": 118287,
                "num_val": 5000,
                "description": "Real-world images with captions"
            }
        }
        
        return datasets_info.get(dataset_name, {})
