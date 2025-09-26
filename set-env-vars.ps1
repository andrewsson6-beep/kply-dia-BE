# PowerShell script to set environment variables in Cloud Run
# Edit the values below and run this script to update your Cloud Run service

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$ServiceName = "kply-dia-api",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1"
)

Write-Host "Setting environment variables for Cloud Run service: $ServiceName" -ForegroundColor Green

# IMPORTANT: Edit these values with your actual configuration
$envVars = @{
    "DATABASE_TYPE" = "postgresql"
    "DATABASE_HOST" = "YOUR_DATABASE_HOST"  # Change this
    "DATABASE_PORT" = "5432"
    "DATABASE_NAME" = "YOUR_DATABASE_NAME"  # Change this
    "DATABASE_USER" = "YOUR_DATABASE_USER"  # Change this
    "DATABASE_SCHEMA" = "public"
    "DATABASE_CHARSET" = "utf8"
    "DATABASE_SSL_MODE" = "require"
    "DATABASE_STATEMENT_CACHE_SIZE" = "0"
    "DATABASE_ECHO" = "false"
    "DATABASE_POOL_ECHO" = "false"
    "HOST" = "0.0.0.0"
    "PORT" = "8080"
    "FASTAPI_API_V1_PATH" = "/api/v1"
    "TOKEN_ALGORITHM" = "HS256"
    "TOKEN_EXPIRE_SECONDS" = "86400"
    "TOKEN_REFRESH_EXPIRE_SECONDS" = "604800"
    "DATETIME_TIMEZONE" = "Asia/Kolkata"
    "DATETIME_FORMAT" = "%Y-%m-%d %H:%M:%S"
    "PROJECT_NAME" = "kply_dialysis"
    "VERSION" = "1.0.0"
    "DEBUG" = "false"
    "GOOGLE_CLIENT_ID" = "YOUR_GOOGLE_CLIENT_ID"  # Change this
}

# Convert to gcloud format
$envVarString = ($envVars.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ","

Write-Host "Updating Cloud Run service with environment variables..." -ForegroundColor Yellow

gcloud run services update $ServiceName `
    --region $Region `
    --set-env-vars $envVarString

if ($LASTEXITCODE -eq 0) {
    Write-Host "Environment variables updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: You still need to set these sensitive variables using Secret Manager:" -ForegroundColor Red
    Write-Host "- DATABASE_PASSWORD" -ForegroundColor Yellow
    Write-Host "- TOKEN_SECRET_KEY" -ForegroundColor Yellow
    Write-Host "- GOOGLE_CLIENT_SECRET" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Example commands to create secrets:" -ForegroundColor Cyan
    Write-Host "gcloud secrets create database-password" -ForegroundColor White
    Write-Host "gcloud secrets create token-secret-key" -ForegroundColor White
    Write-Host "gcloud secrets create google-client-secret" -ForegroundColor White
    Write-Host ""
    Write-Host "Then update the service to use secrets:" -ForegroundColor Cyan
    Write-Host "gcloud run services update $ServiceName --region $Region --set-secrets='DATABASE_PASSWORD=database-password:latest,TOKEN_SECRET_KEY=token-secret-key:latest,GOOGLE_CLIENT_SECRET=google-client-secret:latest'" -ForegroundColor White
} else {
    Write-Host "Failed to update environment variables!" -ForegroundColor Red
}