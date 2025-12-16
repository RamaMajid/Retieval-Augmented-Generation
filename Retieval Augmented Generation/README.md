# Image Retrieval RAG System

An advanced **Retrieval Augmented Generation (RAG)** system for intelligent image search, combining state-of-the-art AI models for image retrieval, captioning, and generation.

![Project Banner](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.9+-green) ![Next.js](https://img.shields.io/badge/Next.js-15-black) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Capabilities
- **🔍 Smart Image Search**: Search by text description or upload similar images using CLIP embeddings
- **🎨 AI-Powered Captions**: Automatic image captioning with BLIP-2 for better understanding
- **✨ Narrative Generation**: Generate coherent narratives from search results using Flan-T5
- **🖼️ Image Generation**: Create new images from text prompts with Stable Diffusion
- **⚡ Fast Vector Search**: Efficient similarity search using FAISS vector database
- **🎯 Multiple Datasets**: Support for Fashion-MNIST, CIFAR-10, COCO, and custom datasets

### Technical Highlights
- **Backend**: FastAPI with Python 3.9+
- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **AI Models**: 
  - CLIP (OpenAI) for image/text embeddings
  - BLIP-2 (Salesforce) for image captioning
  - Flan-T5 (Google) for text generation
  - Stable Diffusion for image generation
- **Vector Database**: FAISS for efficient similarity search
- **Premium UI**: Glassmorphism, smooth animations, responsive design

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 18 or higher
- **GPU** (optional but recommended): CUDA-compatible GPU for faster inference
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: ~10GB for models and datasets

## 🚀 Quick Start

### 1. Clone the Repository

\`\`\`bash
git clone <repository-url>
cd "Retieval Augmented Generation"
\`\`\`

### 2. Backend Setup

\`\`\`bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env file and configure settings
# Set DEVICE=cuda if you have GPU, otherwise DEVICE=cpu
\`\`\`

### 3. Frontend Setup

\`\`\`bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Copy environment file
copy env.txt .env.local

# Edit .env.local if needed (default: http://localhost:8000)
\`\`\`

### 4. Run the Application

**Terminal 1 - Backend:**
\`\`\`bash
cd backend
python app.py
\`\`\`

The backend will start on `http://localhost:8000`

**Terminal 2 - Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

The frontend will start on `http://localhost:3000`

### 5. Load a Dataset

Before searching, you need to load and index a dataset. You can do this via the API:

\`\`\`bash
# Load Fashion-MNIST dataset (default)
curl -X POST http://localhost:8000/api/load-dataset \\
  -H "Content-Type: application/json" \\
  -d '{"dataset_name": "fashion_mnist", "split": "train"}'
\`\`\`

Or use the Python script:

\`\`\`python
from utils import DatasetLoader
from retrieval import SearchEngine
from models import CLIPEncoder

# Initialize components
loader = DatasetLoader()
encoder = CLIPEncoder()
engine = SearchEngine(clip_encoder=encoder)

# Load dataset
image_paths = loader.load_fashion_mnist(split="train")

# Index images
engine.index_images(image_paths, batch_size=32, save_index=True)
\`\`\`

## 📖 Usage Guide

### Text-to-Image Search

1. Open `http://localhost:3000/search`
2. Select **Text Query** mode
3. Enter a description (e.g., "red dress", "sneakers", "t-shirt")
4. Click **Search Images**
5. View results with AI-generated captions and narrative

### Image-to-Image Search

1. Open `http://localhost:3000/search`
2. Select **Image Upload** mode
3. Drag & drop or click to upload an image
4. Click **Find Similar Images**
5. View similar images with similarity scores

### Image Generation

Use the API endpoint to generate images:

\`\`\`bash
curl -X POST http://localhost:8000/api/generate-image \\
  -H "Content-Type: application/json" \\
  -d '{
    "prompt": "a beautiful sunset over mountains",
    "num_images": 1,
    "style": "photorealistic"
  }'
\`\`\`

## 🏗️ Project Structure

\`\`\`
Retieval Augmented Generation/
├── backend/
│   ├── models/
│   │   ├── clip_encoder.py      # CLIP model wrapper
│   │   ├── blip_generator.py    # BLIP-2 captioning
│   │   ├── text_generator.py    # Flan-T5 text generation
│   │   └── diffusion_generator.py # Stable Diffusion
│   ├── retrieval/
│   │   ├── faiss_index.py       # FAISS vector database
│   │   └── search_engine.py     # High-level search engine
│   ├── utils/
│   │   └── dataset_loader.py    # Dataset loading utilities
│   ├── app.py                   # FastAPI application
│   ├── config.py                # Configuration management
│   └── requirements.txt         # Python dependencies
│
└── frontend/
    ├── app/
    │   ├── page.tsx             # Landing page
    │   ├── search/page.tsx      # Search interface
    │   └── globals.css          # Global styles
    ├── components/
    │   ├── ImageUploader.tsx    # Image upload component
    │   ├── TextQueryInput.tsx   # Text search component
    │   ├── ImageGallery.tsx     # Results gallery
    │   ├── GeneratedContent.tsx # Narrative display
    │   └── LoadingSpinner.tsx   # Loading states
    ├── lib/
    │   └── api.ts               # API client
    ├── types/
    │   └── index.ts             # TypeScript types
    └── package.json             # Node dependencies
\`\`\`

## 🔧 Configuration

### Backend Configuration (.env)

\`\`\`env
# Device
DEVICE=cuda  # or cpu

# Model Selection
CLIP_MODEL=openai/clip-vit-base-patch32
BLIP_MODEL=Salesforce/blip2-opt-2.7b
TEXT_GEN_MODEL=google/flan-t5-base
DIFFUSION_MODEL=stabilityai/stable-diffusion-2-1

# Search Parameters
TOP_K_RESULTS=10
MAX_CAPTION_LENGTH=50
MAX_NARRATIVE_LENGTH=200

# Paths
MODEL_CACHE_DIR=./models_cache
FAISS_INDEX_PATH=./data/faiss_index
DATASET_PATH=./data/dataset
\`\`\`

### Frontend Configuration (.env.local)

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

## 📊 Supported Datasets

### Built-in Datasets

1. **Fashion-MNIST** (Default)
   - 60,000 training images
   - 10 classes of fashion items
   - 28x28 grayscale images

2. **CIFAR-10**
   - 50,000 training images
   - 10 classes of objects
   - 32x32 color images

3. **COCO Captions**
   - Real-world images with captions
   - Variable sizes
   - Requires additional setup

### Custom Datasets

Place your images in a directory and load them:

\`\`\`python
from utils import DatasetLoader
loader = DatasetLoader()
image_paths = loader.load_custom_dataset("path/to/your/images")
\`\`\`

## 🎨 UI Features

- **Glassmorphism Design**: Modern frosted glass effects
- **Smooth Animations**: Framer Motion powered transitions
- **Responsive Layout**: Works on mobile, tablet, and desktop
- **Dark Mode**: Eye-friendly dark theme
- **Loading States**: Beautiful skeleton loaders and spinners
- **Typewriter Effect**: Animated text generation display
- **Image Modal**: Expandable image viewer with details

## 🚀 API Endpoints

### Search Endpoints

- `POST /api/search-by-text` - Search images using text query
- `POST /api/search-by-image` - Search images using uploaded image

### Generation Endpoints

- `POST /api/generate-image` - Generate images from text prompt
- `POST /api/generate-from-captions` - Generate images from captions

### Dataset Endpoints

- `POST /api/load-dataset` - Load and index a dataset
- `GET /api/dataset-info` - Get current dataset information

### Utility Endpoints

- `GET /api/health` - Health check
- `GET /api/image/{path}` - Serve image files

## 🔬 How It Works

1. **Image Encoding**: CLIP converts images to 512-dimensional embeddings
2. **Vector Storage**: FAISS stores embeddings for fast similarity search
3. **Search**: Query (text or image) is encoded and compared with stored embeddings
4. **Retrieval**: Top-K most similar images are retrieved
5. **Caption Generation**: BLIP-2 generates captions for retrieved images
6. **Narrative Generation**: Flan-T5 creates a coherent narrative from captions
7. **Image Generation** (optional): Stable Diffusion creates new images

## 🛠️ Troubleshooting

### Backend Issues

**Models not loading:**
- Ensure you have enough RAM (8GB minimum)
- Check internet connection for model downloads
- Models are cached in `./models_cache`

**CUDA out of memory:**
- Set `DEVICE=cpu` in `.env`
- Reduce batch size in dataset loading
- Use smaller models (e.g., `blip2-opt-2.7b` instead of larger variants)

### Frontend Issues

**API connection failed:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend/config.py`
- Verify `.env.local` has correct API URL

**Images not displaying:**
- Check `next.config.ts` has correct image domains
- Ensure backend image serving endpoint is working

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🙏 Acknowledgments

- **OpenAI** for CLIP
- **Salesforce** for BLIP-2
- **Google** for Flan-T5
- **Stability AI** for Stable Diffusion
- **Facebook Research** for FAISS

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using cutting-edge AI technologies**
