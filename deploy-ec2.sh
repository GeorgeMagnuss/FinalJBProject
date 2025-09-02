#!/bin/bash

# AWS EC2 Deployment Script for Vacation Management System
# Run this script on your EC2 instance

echo "🚀 Starting deployment of Vacation Management System..."

# Clean up existing deployment
if [ -d "FinalJBProject" ]; then
    echo "📂 Found existing FinalJBProject directory, cleaning up..."
    cd FinalJBProject
    sudo docker-compose down --volumes --remove-orphans
    cd ..
    sudo rm -rf FinalJBProject
fi

# Clone latest version
echo "📥 Cloning latest code from GitHub..."
git clone https://github.com/GeorgeMagnuss/FinalJBProject.git
cd FinalJBProject

# Pull Docker images
echo "🐳 Pulling Docker images from DockerHub..."
sudo docker pull georgem94/vacation-website:latest
sudo docker pull georgem94/stats-backend:latest  
sudo docker pull georgem94/stats-frontend:latest
sudo docker pull postgres:15

# Start services
echo "▶️  Starting all services..."
sudo docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check service status
echo "🔍 Checking service status..."
sudo docker-compose ps

# Show access information
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access your applications:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "🔑 Admin credentials:"
echo "   Email: admin@vacation.com"
echo "   Password: admin123"
echo ""
echo "📊 API Endpoints:"
echo "   Stats API: http://$EC2_IP:8001/api/"
echo ""