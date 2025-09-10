#!/bin/bash

# Band-Logo Processing Tool - Docker Deployment Script
echo "🎵 Building Band-Logo Processing Tool..."

# Build the Docker image
docker build -t band-logo-tool .

if [ $? -eq 0 ]; then
    echo "✅ Build successful! Starting container..."
    
    # Stop existing container if running
    docker stop imagescale-app 2>/dev/null || true
    docker rm imagescale-app 2>/dev/null || true
    
    # Run the container on port 8724
    docker run -d -p 8724:8724 --name imagescale-app band-logo-tool
    
    if [ $? -eq 0 ]; then
        echo "🚀 Application is running!"
        echo "📱 Access at: http://localhost:8724"
        echo "🎯 For radio-endstation.de: http://radio-endstation.de:8724"
        echo ""
        echo "📋 Container status:"
        docker ps | grep imagescale-app
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "❌ Build failed"
    exit 1
fi
