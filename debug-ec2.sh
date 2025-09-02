#!/bin/bash

# Debug EC2 issues
echo "🔍 Debugging EC2 deployment..."

EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "🌐 EC2 IP: $EC2_IP"

# Check if services are running
echo "📊 Service status:"
sudo docker-compose ps

# Check logs for authentication issues
echo ""
echo "📋 Stats backend logs (last 20 lines):"
sudo docker-compose logs --tail=20 stats_backend

echo ""
echo "📋 Vacation website logs (last 20 lines):"
sudo docker-compose logs --tail=20 vacation_website

# Test database connection
echo ""
echo "🔍 Testing database connection:"
sudo docker-compose exec db psql -U postgres -d vacation_db -c "SELECT email, is_staff, is_superuser FROM users WHERE email='admin@example.com';"

# Test admin user in vacation website
echo ""
echo "🔍 Testing admin user in vacation website:"
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User
try:
    admin = User.objects.get(email='admin@example.com')
    print(f'✅ Found admin: {admin.email}')
    print(f'Is admin: {admin.is_admin}')
    print(f'Is staff: {admin.is_staff}')
    print(f'Is active: {admin.is_active}')
    print(f'Password check: {admin.check_password(\"adminpass\")}')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Test admin user in stats backend
echo ""
echo "🔍 Testing admin user in stats backend:"
sudo docker-compose exec stats_backend python manage.py shell -c "
from stats.models import User
try:
    admin = User.objects.get(email='admin@example.com')
    print(f'✅ Found admin: {admin.email}')
    print(f'Is admin: {admin.is_admin}')
    print(f'Is staff: {admin.is_staff}')
    print(f'Is active: {admin.is_active}')
    print(f'Password check: {admin.check_password(\"adminpass\")}')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Check media files
echo ""
echo "🖼️  Checking media files:"
sudo docker-compose exec vacation_website ls -la /app/media/

# Test media URL access
echo ""
echo "🌐 Testing media URL access:"
curl -I http://$EC2_IP:8000/media/telaviv.jpg

echo ""
echo "🔗 Test URLs:"
echo "   Vacation: http://$EC2_IP:8000"
echo "   Stats: http://$EC2_IP:3000"
echo "   Direct API test: curl -X POST http://$EC2_IP:8001/api/login/ -H 'Content-Type: application/json' -d '{\"email\":\"admin@example.com\",\"password\":\"adminpass\"}'"