#!/bin/bash
set -e

echo "🚀 Starting vacation website deployment..."

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose pull

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start all services
echo "▶️ Starting all services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo "✅ Deployment complete!"
echo ""
echo "🌐 Services available at:"
echo "  - Main website: http://localhost:8000"
echo "  - Stats backend: http://localhost:8001"  
echo "  - Stats frontend: http://localhost:3000"
echo ""
echo "🔐 Admin credentials:"
echo "  - Email: admin@vacation.com"
echo "  - Password: admin123"