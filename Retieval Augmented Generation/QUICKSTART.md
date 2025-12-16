# Quick Start Guide

## Frontend

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Create environment file:**
   ```bash
   # Copy env.txt to .env.local
   copy env.txt .env.local
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   Navigate to `http://localhost:3000`

## Backend

### Option 1: Using setup script (Recommended for Windows)

1. **Run setup:**
   ```bash
   cd backend
   setup.bat
   ```

2. **Start server:**
   ```bash
   run.bat
   ```

### Option 2: Manual setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   copy .env.example .env
   ```

5. **Initialize system (load dataset):**
   ```bash
   python initialize.py
   ```
   This will download models and index the first 1000 images from Fashion-MNIST.

6. **Start server:**
   ```bash
   python app.py
   ```

## Troubleshooting

### Frontend Issues

**Error: Cannot apply unknown utility class**
- This has been fixed. Make sure you have the latest `globals.css` file.
- Try deleting `.next` folder and running `npm run dev` again.

**Images not loading:**
- Make sure backend is running on `http://localhost:8000`
- Check that dataset has been loaded

### Backend Issues

**ModuleNotFoundError: No module named 'torch'**
- Make sure you're using the virtual environment
- Run `venv\Scripts\activate` before running Python commands

**CUDA out of memory:**
- Edit `.env` and set `DEVICE=cpu`
- Reduce batch size in dataset loading

**Models downloading slowly:**
- Models are ~5GB total, first run will take time
- Models are cached in `models_cache` folder

## Quick Test

After both servers are running:

1. Open `http://localhost:3000`
2. Click "Start Searching"
3. Try text query: "sneakers" or "dress"
4. View results with AI-generated captions

## Notes

- Backend needs to load dataset before searching works
- First run downloads models (~5GB)
- GPU recommended but not required
- Minimum 8GB RAM recommended
