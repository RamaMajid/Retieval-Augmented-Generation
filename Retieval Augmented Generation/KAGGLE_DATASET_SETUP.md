# 📦 Kaggle Fashion Dataset Setup Guide

## 🎯 Quick Start

### Step 1: Download Dataset

**Option A: Using Kaggle CLI** (Recommended)
```bash
# Install Kaggle CLI
pip install kaggle

# Setup API credentials (one-time)
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token"
# 3. Save kaggle.json to ~/.kaggle/ (Linux/Mac) or C:\Users\<username>\.kaggle\ (Windows)

# Download dataset
kaggle datasets download -d nirmalsankalana/fashion-product-text-images-dataset

# Extract
unzip fashion-product-text-images-dataset.zip -d backend/data/kaggle_fashion/
```

**Option B: Manual Download**
1. Visit: https://www.kaggle.com/datasets/nirmalsankalana/fashion-product-text-images-dataset
2. Click **"Download"** button (requires Kaggle login)
3. Extract ZIP to: `backend/data/kaggle_fashion/`

### Step 2: Verify Structure

Your folder should look like:
```
backend/data/kaggle_fashion/
├── images/
│   ├── 1001.jpg
│   ├── 1002.jpg
│   └── ... (thousands of images)
└── styles.csv (metadata)
```

### Step 3: Clean Old Data (Optional)

**Safe to delete:**
```bash
# Delete old Fashion-MNIST data
rm -rf backend/data/dataset/
rm -rf backend/data/faiss_index/
```

**Keep these:**
- `backend/models_cache/` (your downloaded models)
- `backend/.env` (your configuration)

### Step 4: Load New Dataset

**Via Swagger UI:**
1. Open: http://localhost:8000/docs
2. Find: `POST /api/load-dataset`
3. Click "Try it out"
4. Use this JSON:
```json
{
  "dataset_name": "kaggle_fashion",
  "split": "train"
}
```
5. Click "Execute"
6. Wait 5-10 minutes (indexing)

**Via curl:**
```bash
curl -X POST http://localhost:8000/api/load-dataset \
  -H "Content-Type: application/json" \
  -d '{"dataset_name": "kaggle_fashion", "split": "train"}'
```

### Step 5: Test Search

Try these queries:
- "red dress"
- "blue jeans"  
- "leather jacket"
- "white sneakers"
- "summer dress"

---

## 📊 Dataset Info

**Size:** ~2-3GB (44,000+ images)
**Categories:** Apparel, Footwear, Accessories
**Format:** JPG images + CSV metadata
**Quality:** Real product photos (high quality)

---

## ⚠️ Troubleshooting

**"Dataset not found" error:**
- Check folder path: `backend/data/kaggle_fashion/`
- Verify `images/` folder and `styles.csv` exist

**"Out of memory" during indexing:**
- Reduce batch size in code
- Or index in smaller chunks

**Slow indexing:**
- Normal for large dataset
- ~1000 images per minute on CPU
- Use GPU for 5x faster indexing

---

## 🎉 Benefits

✅ Real product images (vs synthetic MNIST)
✅ Better BLIP-2 captions
✅ More diverse categories
✅ Professional product photos
✅ Metadata with descriptions

---

Need help? Check the implementation plan for detailed steps!
