#!/bin/bash

# OpthalmoAI Backend Cloud Deployment Script
# This script deploys the backend to Google Cloud Run

echo "🚀 Deploying OpthalmoAI Backend to Google Cloud Run..."

# Set variables
PROJECT_ID="opthalmoai"
SERVICE_NAME="opthalmoai-backend"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Build and push Docker image
echo "📦 Building Docker image..."
docker build -f Dockerfile.cloud -t $IMAGE_NAME .

echo "📤 Pushing image to Google Container Registry..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo "🌐 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 5 \
  --port 8004 \
  --set-env-vars "PORT=8004,PYTHONPATH=/app" \
  --project $PROJECT_ID

echo "✅ Deployment complete!"
echo "🔗 Backend URL will be provided by Cloud Run"