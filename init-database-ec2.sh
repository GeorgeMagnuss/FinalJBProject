#!/bin/bash

# Database initialization script for EC2
echo "🗄️  Initializing database for EC2 deployment..."

# Stop containers if running
sudo docker-compose down

# Remove existing database volume to start fresh
echo "🧹 Cleaning database volume..."
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true

# Start only database first
echo "📊 Starting PostgreSQL database..."
sudo docker-compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 20

# Check if database is ready
until sudo docker-compose exec db pg_isready -U postgres; do
    echo "Waiting for database..."
    sleep 2
done

echo "✅ Database is ready!"

# Run migrations and populate data for vacation website
echo "🏖️  Setting up vacation website database..."
sudo docker-compose exec vacation_website python manage.py migrate --run-syncdb
sudo docker-compose exec vacation_website python manage.py populate_db

# Run migrations for stats website  
echo "📈 Setting up stats website database..."
sudo docker-compose exec stats_backend python manage.py migrate --run-syncdb

# Start all services
echo "🚀 Starting all services..."
sudo docker-compose up -d

# Final status check
sleep 10
echo "📊 Final service status:"
sudo docker-compose ps

EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo ""
echo "✅ Database initialization complete!"
echo ""
echo "🌐 Test your applications:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"