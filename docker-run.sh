#!/bin/bash

# Band-Logo Processing Tool - Docker Deployment Script
echo "🎵 Starting Band-Logo Processing Tool deployment..."

# Update from Git repository
echo "📥 Updating from Git repository..."
git fetch origin
git reset --hard origin/main

if [ $? -eq 0 ]; then
    echo "✅ Git update successful!"
    # Fix permissions after git reset
    echo "🔧 Fixing file permissions..."
    chmod +x docker-run.sh
    chmod +x docker-run.bat
else
    echo "⚠️  Git update failed, continuing with current version..."
fi

echo "🔨 Building Band-Logo Processing Tool..."

# Build the Docker image
docker build -t band-logo-tool .

if [ $? -eq 0 ]; then
    echo "✅ Build successful! Starting container..."
    
    # Stop existing container if running
    echo "🛑 Stopping existing container..."
    docker stop imagescale-app 2>/dev/null || true
    docker rm imagescale-app 2>/dev/null || true
    
    # Run the container on port 8724
    echo "🚀 Starting new container..."
    docker run -d -p 8724:8724 --name imagescale-app band-logo-tool
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 SUCCESS! Application is running!"
        echo "📱 Local access: http://localhost:8724"
        echo "🌐 Server access: http://$(hostname -I | awk '{print $1}'):8724"
        echo "🎯 For radio-endstation.de: http://radio-endstation.de:8724"
        echo ""
        echo "📋 Container status:"
        docker ps | grep imagescale-app
        echo ""
        echo "📝 To check logs: docker logs imagescale-app"
        echo "🛑 To stop: docker stop imagescale-app"
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "❌ Build failed"
    exit 1
fi
