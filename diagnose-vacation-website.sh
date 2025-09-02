#!/bin/bash

# Diagnose vacation website startup issues
echo "🔍 Diagnosing vacation website startup issues..."

EC2_IP="13.53.38.63"
cd FinalJBProject

# Stop all services first
echo "🛑 Stopping all services..."
sudo docker-compose down

# Start only database and wait
echo "📊 Starting database..."
sudo docker-compose up -d db

echo "⏳ Waiting for database to be healthy..."
sleep 30

# Check database health
sudo docker-compose exec db pg_isready -U postgres
echo "✅ Database is ready"

# Now start vacation website in FOREGROUND mode to see logs
echo ""
echo "🏖️  Starting vacation website in FOREGROUND mode..."
echo "👀 Watch for any error messages below:"
echo "----------------------------------------"

# Run vacation website in foreground to see live logs
sudo docker-compose up vacation_website

# This will show live logs and any startup errors
# The script will stop here until you press Ctrl+C