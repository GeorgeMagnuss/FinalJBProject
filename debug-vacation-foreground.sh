#!/bin/bash

# Debug vacation website by running in foreground
echo "🔍 Running vacation website in foreground to see errors..."

cd FinalJBProject

# Stop all services
sudo docker-compose down

# Start database
echo "📊 Starting database..."
sudo docker-compose up -d db

# Wait for database
sleep 30

# Run vacation website in foreground to see live logs
echo ""
echo "🏖️  Starting vacation website in FOREGROUND..."
echo "👀 Watch for Django startup errors below:"
echo "========================================="
echo ""

# This will show live logs - any errors will be visible
sudo docker-compose up vacation_website

# When you see the error, press Ctrl+C to stop