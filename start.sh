#!/bin/bash

echo "🚀 Starting Chat with PDF Application"
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "🔧 Building and starting services..."

# Build and start the services
docker-compose up --build

echo "🎉 Application started successfully!"
echo "📱 Frontend (Streamlit): http://localhost:8501"
echo "🔧 Backend (FastAPI): http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the application, press Ctrl+C"
