# Deployment Guide

This guide covers deploying the Image Retrieval RAG system to production.

## Backend Deployment

### Option 1: Docker Deployment

1. **Create Dockerfile** (`backend/Dockerfile`):

\`\`\`dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

2. **Build and run:**

\`\`\`bash
cd backend
docker build -t image-rag-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data image-rag-backend
\`\`\`

### Option 2: Cloud Platforms

#### Google Cloud Run

\`\`\`bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/image-rag-backend

# Deploy
gcloud run deploy image-rag-backend \\
  --image gcr.io/PROJECT_ID/image-rag-backend \\
  --platform managed \\
  --region us-central1 \\
  --memory 4Gi \\
  --cpu 2
\`\`\`

#### AWS EC2

1. Launch EC2 instance (t3.large or larger)
2. Install Python and dependencies
3. Use systemd for process management:

\`\`\`bash
# /etc/systemd/system/image-rag.service
[Unit]
Description=Image RAG Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/backend
ExecStart=/home/ubuntu/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
\`\`\`

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI:**

\`\`\`bash
npm install -g vercel
\`\`\`

2. **Deploy:**

\`\`\`bash
cd frontend
vercel
\`\`\`

3. **Set environment variables in Vercel dashboard:**
   - `NEXT_PUBLIC_API_URL`: Your backend URL

### Option 2: Netlify

1. **Build the project:**

\`\`\`bash
cd frontend
npm run build
\`\`\`

2. **Deploy to Netlify:**

\`\`\`bash
npm install -g netlify-cli
netlify deploy --prod --dir=.next
\`\`\`

### Option 3: Self-hosted

1. **Build for production:**

\`\`\`bash
cd frontend
npm run build
npm start
\`\`\`

2. **Use PM2 for process management:**

\`\`\`bash
npm install -g pm2
pm2 start npm --name "image-rag-frontend" -- start
pm2 save
pm2 startup
\`\`\`

## Performance Optimization

### Backend Optimizations

1. **Use GPU for inference:**
   - Set `DEVICE=cuda` in `.env`
   - Use GPU-enabled cloud instances

2. **Model optimization:**
   - Use quantized models for faster inference
   - Enable model caching

3. **FAISS optimization:**
   - Use `faiss-gpu` for GPU acceleration
   - Use IVF or HNSW indices for large datasets

### Frontend Optimizations

1. **Enable Next.js optimizations:**
   - Image optimization is already enabled
   - Use static generation where possible

2. **CDN deployment:**
   - Deploy static assets to CDN
   - Use edge functions for API routes

## Monitoring

### Backend Monitoring

1. **Add logging:**

\`\`\`python
import logging
logging.basicConfig(level=logging.INFO)
\`\`\`

2. **Use monitoring tools:**
   - Prometheus for metrics
   - Grafana for visualization
   - Sentry for error tracking

### Frontend Monitoring

1. **Add analytics:**
   - Google Analytics
   - Vercel Analytics

2. **Error tracking:**
   - Sentry
   - LogRocket

## Security Considerations

1. **API Security:**
   - Add authentication (JWT, OAuth)
   - Rate limiting
   - Input validation

2. **CORS Configuration:**
   - Update `CORS_ORIGINS` in backend config
   - Use environment variables for production URLs

3. **Environment Variables:**
   - Never commit `.env` files
   - Use secrets management (AWS Secrets Manager, etc.)

## Scaling

### Horizontal Scaling

1. **Load balancer:**
   - Use nginx or cloud load balancer
   - Distribute traffic across multiple backend instances

2. **Database:**
   - Use shared storage for FAISS index
   - Consider vector databases (Milvus, Pinecone)

### Vertical Scaling

1. **Increase resources:**
   - More RAM for larger models
   - Better GPU for faster inference
   - More CPU cores for parallel processing

## Backup and Recovery

1. **Backup FAISS index:**
   - Regular backups of `data/faiss_index`
   - Store in cloud storage (S3, GCS)

2. **Model caching:**
   - Cache downloaded models
   - Use persistent storage

## Cost Optimization

1. **Model selection:**
   - Use smaller models for lower costs
   - Balance performance vs. cost

2. **Auto-scaling:**
   - Scale down during low traffic
   - Use serverless for intermittent workloads

3. **Caching:**
   - Cache frequent queries
   - Use CDN for static assets
