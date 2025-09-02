#!/bin/bash

# Fix script for EC2 deployment issues
echo "🔧 Fixing EC2 deployment issues..."

# Stop any running containers
echo "🛑 Stopping existing containers..."
sudo docker-compose down --volumes --remove-orphans 2>/dev/null || true

# Kill any processes using the ports
echo "🔌 Freeing up ports..."
sudo fuser -k 5432/tcp 2>/dev/null || true
sudo fuser -k 5433/tcp 2>/dev/null || true
sudo fuser -k 8000/tcp 2>/dev/null || true
sudo fuser -k 8001/tcp 2>/dev/null || true
sudo fuser -k 3000/tcp 2>/dev/null || true

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Update docker-compose.yml to use standard PostgreSQL port
echo "⚙️  Updating docker-compose.yml..."
sed -i 's/5433:5432/5432:5432/g' docker-compose.yml

# Remove any existing containers and volumes
echo "🧹 Cleaning up Docker resources..."
sudo docker system prune -f
sudo docker volume prune -f

# Pull fresh images
echo "🐳 Pulling fresh Docker images..."
sudo docker pull georgem94/vacation-website:latest
sudo docker pull georgem94/stats-backend:latest
sudo docker pull georgem94/stats-frontend:latest
sudo docker pull postgres:15

# Start deployment
echo "🚀 Starting deployment..."
sudo docker-compose up -d

# Wait and check status
sleep 30
echo "📊 Service status:"
sudo docker-compose ps

# Show access info
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "YOUR_EC2_IP")
echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access URLs:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "🔑 Admin Login:"
echo "   Email: admin@vacation.com"
echo "   Password: admin123"