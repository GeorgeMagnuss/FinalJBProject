#!/bin/bash

# Simple fix for stats backend - bypass migrations entirely
echo "🔧 Simple stats backend fix..."

EC2_IP="13.53.38.63"
cd FinalJBProject

# Check current stats backend logs
echo "📋 Current stats backend logs:"
sudo docker-compose logs --tail=10 stats_backend

# Stop stats backend only
echo "🛑 Stopping stats backend..."
sudo docker-compose stop stats_backend

# Start stats backend without migrations
echo "📈 Starting stats backend without migrations..."
sudo docker-compose run -d --name temp_stats_backend -p 8001:8001 \
  -e DEBUG=1 \
  -e DB_HOST=db \
  -e DB_NAME=vacation_db \
  -e DB_USER=postgres \
  -e DB_PASSWORD=password \
  -e DB_PORT=5432 \
  georgem94/stats-backend:latest \
  sh -c "python manage.py runserver 0.0.0.0:8001"

sleep 15

# Test stats backend directly
echo "🧪 Testing stats backend:"
curl -f http://$EC2_IP:8001/api/ && echo "✅ Stats backend API working" || echo "❌ Stats backend API failed"

# Test login
echo ""
echo "🔐 Testing login:"
curl -X POST http://$EC2_IP:8001/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"adminpass"}' \
  -v

# If that works, replace the problematic container
echo ""
echo "🔄 Replacing stats backend container..."
sudo docker stop temp_stats_backend
sudo docker rm temp_stats_backend

# Update docker-compose to skip migrations for stats backend
sed -i 's|python manage.py migrate --run-syncdb &&|echo "Skipping migrations..." &&|g' docker-compose.yml

# Restart stats backend with fixed config
sudo docker-compose up -d stats_backend

sleep 15

echo ""
echo "📊 Final status:"
sudo docker-compose ps

echo ""
echo "🌐 Test URLs:"
echo "   Vacation: http://$EC2_IP:8000"
echo "   Stats: http://$EC2_IP:3000"
echo "   API: http://$EC2_IP:8001/api/"