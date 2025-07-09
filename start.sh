#!/bin/bash

# Google Analytics Dashboard - Quick Start Script
echo "🚀 Starting Google Analytics Dashboard..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Created .env file"
        echo "⚠️  Please edit .env file with your Google Analytics credentials before continuing"
        echo "   - Add your GA4 Property ID"
        echo "   - Add your service account JSON credentials"
        echo ""
        echo "Press Enter when you've configured .env file..."
        read
    else
        echo "❌ env.example file not found"
        exit 1
    fi
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🌐 Starting the application..."
    echo "   The app will be available at: http://localhost:8501"
    echo "   Press Ctrl+C to stop the application"
    echo ""
    
    # Start the application
    docker-compose up
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi 