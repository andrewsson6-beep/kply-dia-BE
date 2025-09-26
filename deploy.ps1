# PowerShell deployment script for kply-dia-BE
# Run this script from the project root directory

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$ImageName = "kply-dia-be",
    
    [Parameter(Mandatory=$false)]
    [string]$ServiceName = "kply-dia-api",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1",
    
    [Parameter(Mandatory=$false)]
    [string]$ImageTag = "latest"
)

Write-Host "Starting deployment for project: $ProjectId" -ForegroundColor Green

# Step 1: Configure Docker for GCR
Write-Host "Configuring Docker for GCR..." -ForegroundColor Yellow
gcloud auth configure-docker

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to configure Docker. Please check your gcloud authentication." -ForegroundColor Red
    exit 1
}

# Step 2: Build Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
$imageName = "gcr.io/$ProjectId/$ImageName" + ":" + $ImageTag
docker build -t $imageName .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

# Step 3: Push to GCR
Write-Host "Pushing image to Google Container Registry..." -ForegroundColor Yellow
docker push $imageName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker push failed!" -ForegroundColor Red
    exit 1
}

# Step 4: Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow

# Check if .env file exists for reference
if (Test-Path ".env") {
    Write-Host "Found .env file. Please ensure you set the environment variables in Cloud Run." -ForegroundColor Cyan
} else {
    Write-Host "No .env file found. Please create one from .env.example and set environment variables manually." -ForegroundColor Yellow
}

# Basic deployment command (you'll need to add your specific environment variables)
gcloud run deploy $ServiceName `
    --image $imageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --port 8080 `
    --memory 1Gi `
    --cpu 1 `
    --min-instances 0 `
    --max-instances 10

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment successful!" -ForegroundColor Green
    
    # Get the service URL
    $serviceUrl = gcloud run services describe $ServiceName --region $Region --format="value(status.url)"
    Write-Host "Your service is available at: $serviceUrl" -ForegroundColor Cyan
    Write-Host "API docs available at: $serviceUrl/docs" -ForegroundColor Cyan
} else {
    Write-Host "Deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Don't forget to:" -ForegroundColor Yellow
Write-Host "1. Set your environment variables in Cloud Run console or using gcloud commands" -ForegroundColor White
Write-Host "2. Configure your database connection" -ForegroundColor White
Write-Host "3. Set up Google OAuth credentials" -ForegroundColor White
Write-Host "4. Update CORS settings if needed" -ForegroundColor White