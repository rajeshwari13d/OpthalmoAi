@echo off
echo ========================================
echo OpthalmoAI Backend Deployment Script
echo ========================================

echo.
echo [1/6] Checking prerequisites...
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again
    pause
    exit /b 1
)

where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Google Cloud CLI is not installed
    echo Please install gcloud CLI and try again
    pause
    exit /b 1
)

echo.
echo [2/6] Building Docker image...
cd /d "%~dp0..\backend"
docker build -t opthalmoai-backend:latest .
if %errorlevel% neq 0 (
    echo ERROR: Docker build failed
    pause
    exit /b 1
)

echo.
echo [3/6] Tagging image for Google Cloud...
set /p PROJECT_ID=Enter your Google Cloud Project ID: 
docker tag opthalmoai-backend:latest gcr.io/%PROJECT_ID%/opthalmoai-backend:latest

echo.
echo [4/6] Pushing to Google Container Registry...
docker push gcr.io/%PROJECT_ID%/opthalmoai-backend:latest
if %errorlevel% neq 0 (
    echo ERROR: Docker push failed
    echo Make sure you're authenticated with: gcloud auth configure-docker
    pause
    exit /b 1
)

echo.
echo [5/6] Deploying to Cloud Run...
gcloud run deploy opthalmoai-api ^
    --image gcr.io/%PROJECT_ID%/opthalmoai-backend:latest ^
    --platform managed ^
    --region us-central1 ^
    --allow-unauthenticated ^
    --memory 2Gi ^
    --cpu 2 ^
    --max-instances 10 ^
    --port 8000 ^
    --set-env-vars ENVIRONMENT=production

if %errorlevel% neq 0 (
    echo ERROR: Cloud Run deployment failed
    pause
    exit /b 1
)

echo.
echo [6/6] Getting service URL...
for /f "tokens=*" %%i in ('gcloud run services describe opthalmoai-api --region us-central1 --format="value(status.url)"') do set SERVICE_URL=%%i

echo.
echo ========================================
echo ✅ DEPLOYMENT SUCCESSFUL!
echo ========================================
echo.
echo Backend API URL: %SERVICE_URL%
echo.
echo Next steps:
echo 1. Update frontend API configuration with: %SERVICE_URL%
echo 2. Test the API health endpoint: %SERVICE_URL%/api/v1/health
echo 3. Update CORS settings if needed
echo.
pause