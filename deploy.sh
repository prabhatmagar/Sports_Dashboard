#!/bin/bash

# Sports Dashboard Deployment Script for Digital Ocean

echo "🚀 Deploying Sports Dashboard to Digital Ocean..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one with your API keys."
    echo "Example .env file:"
    echo "API_SPORTS_KEY=your_api_key_here"
    echo "RAPIDAPI_KEY=your_rapidapi_key_here"
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t sports-dashboard .

# Tag for Digital Ocean Container Registry
echo "🏷️ Tagging image for Digital Ocean..."
docker tag sports-dashboard registry.digitalocean.com/your-registry/sports-dashboard:latest

# Push to Digital Ocean Container Registry
echo "⬆️ Pushing to Digital Ocean Container Registry..."
docker push registry.digitalocean.com/your-registry/sports-dashboard:latest

# Deploy to Digital Ocean App Platform
echo "🚀 Deploying to Digital Ocean App Platform..."
doctl apps create-deployment your-app-id --force-rebuild

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at: https://your-app-name.ondigitalocean.app"
