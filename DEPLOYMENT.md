# Cloud Deployment Guide for kply-dia-BE

## Prerequisites
1. Install Docker Desktop
2. Install Google Cloud SDK (gcloud CLI)
3. Authenticate with Google Cloud: `gcloud auth login`
4. Set your Google Cloud project: `gcloud config set project YOUR_PROJECT_ID`
5. Enable required APIs:
   ```powershell
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

## Step 1: Configure Docker for GCR
```powershell
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker
```

## Step 2: Set Environment Variables
```powershell
# Set your project variables
$PROJECT_ID = "your-gcp-project-id"
$IMAGE_NAME = "kply-dia-be"
$SERVICE_NAME = "kply-dia-api"
$REGION = "us-central1"  # or your preferred region
$IMAGE_TAG = "latest"
```

## Step 3: Build Docker Image
```powershell
# Navigate to your project directory
cd "d:\Other\kply-dia-BE"

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG .

# Alternative with explicit tag
docker build -t gcr.io/your-gcp-project-id/kply-dia-be:latest .
```

## Step 4: Test Docker Image Locally (Optional)
```powershell
# Create a local .env file from .env.example first
cp .env.example .env
# Edit .env with your actual values

# Run locally to test
docker run -p 8080:8080 --env-file .env gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG
```

## Step 5: Push to Google Container Registry
```powershell
# Push the image to GCR
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG

# Alternative explicit command
docker push gcr.io/your-gcp-project-id/kply-dia-be:latest
```

## Step 6: Deploy to Cloud Run
```powershell
# Deploy with environment variables from your .env file
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --port 8080 `
  --memory 1Gi `
  --cpu 1 `
  --min-instances 0 `
  --max-instances 10 `
  --set-env-vars "DATABASE_TYPE=postgresql,DATABASE_SSL_MODE=require,HOST=0.0.0.0,PORT=8080,FASTAPI_API_V1_PATH=/api/v1,DATETIME_TIMEZONE=Asia/Kolkata" `
  --set-env-vars "DATABASE_HOST=YOUR_DB_HOST,DATABASE_PORT=5432,DATABASE_NAME=YOUR_DB_NAME,DATABASE_USER=YOUR_DB_USER,DATABASE_SCHEMA=public" `
  --set-env-vars "TOKEN_ALGORITHM=HS256,DATABASE_STATEMENT_CACHE_SIZE=0,DATABASE_ECHO=false,DATABASE_POOL_ECHO=false"

# For sensitive environment variables, use Secret Manager:
# First create secrets:
gcloud secrets create database-password --data-file=-  # Enter password when prompted
gcloud secrets create database-url --data-file=-       # Enter full DB URL when prompted
gcloud secrets create token-secret-key --data-file=-   # Enter JWT secret when prompted
gcloud secrets create google-client-secret --data-file=-  # Enter Google OAuth secret when prompted

# Then deploy with secrets:
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --port 8080 `
  --memory 1Gi `
  --cpu 1 `
  --min-instances 0 `
  --max-instances 10 `
  --set-env-vars "DATABASE_TYPE=postgresql,DATABASE_SSL_MODE=require,HOST=0.0.0.0,PORT=8080" `
  --set-env-vars "DATABASE_HOST=YOUR_DB_HOST,DATABASE_PORT=5432,DATABASE_NAME=YOUR_DB_NAME,DATABASE_USER=YOUR_DB_USER" `
  --set-env-vars "GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID" `
  --set-secrets "DATABASE_PASSWORD=database-password:latest" `
  --set-secrets "DATABASE_URL=database-url:latest" `
  --set-secrets "TOKEN_SECRET_KEY=token-secret-key:latest" `
  --set-secrets "GOOGLE_CLIENT_SECRET=google-client-secret:latest"
```

## Step 7: Update Service (for subsequent deployments)
```powershell
# Rebuild and push new image
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG .
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG

# Update the service
gcloud run services update $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG `
  --region $REGION
```

## Step 8: Environment Variables Checklist
Make sure to set these environment variables in Cloud Run:

### Required Variables:
- `DATABASE_TYPE` (postgresql)
- `DATABASE_HOST` (your database host)
- `DATABASE_PORT` (5432)
- `DATABASE_NAME` (your database name)
- `DATABASE_USER` (your database user)
- `DATABASE_PASSWORD` (use Secret Manager)
- `DATABASE_SCHEMA` (public)
- `TOKEN_SECRET_KEY` (use Secret Manager)
- `TOKEN_ALGORITHM` (HS256)
- `GOOGLE_CLIENT_ID` (your OAuth client ID)
- `GOOGLE_CLIENT_SECRET` (use Secret Manager)

### Optional Variables:
- `DATABASE_URL` (alternative to individual DB params)
- `DATABASE_SSL_MODE` (require/verify-full)
- `DEBUG` (false for production)
- `PROJECT_NAME` (kply_dialysis)
- `VERSION` (1.0.0)

## Useful Commands:
```powershell
# View logs
gcloud run logs tail $SERVICE_NAME --region $REGION

# Get service URL
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"

# List deployments
gcloud run services list --region $REGION

# Delete service
gcloud run services delete $SERVICE_NAME --region $REGION
```

## Security Best Practices:
1. Use Google Secret Manager for sensitive data (passwords, API keys, JWT secrets)
2. Enable IAM authentication if you don't need public access
3. Use Cloud SQL for production databases with SSL
4. Set up proper CORS origins for your frontend domains
5. Use minimum required CPU/memory allocations
6. Enable Cloud Run audit logs