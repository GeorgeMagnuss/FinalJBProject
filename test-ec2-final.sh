#!/bin/bash

# Final EC2 testing script
echo "🧪 Final EC2 Testing..."

EC2_IP="13.53.38.63"

# Wait a bit more for stats backend to fully start
sleep 10

echo "📊 Service Status:"
sudo docker-compose ps

echo ""
echo "🔍 Testing all endpoints:"

# Test vacation website
echo "Testing vacation website (port 8000):"
curl -f http://$EC2_IP:8000/ > /dev/null 2>&1 && echo "✅ Vacation website accessible" || echo "❌ Vacation website failed"

# Test stats backend API
echo "Testing stats backend API (port 8001):"
curl -f http://$EC2_IP:8001/api/ > /dev/null 2>&1 && echo "✅ Stats API accessible" || echo "❌ Stats API failed"

# Test stats frontend
echo "Testing stats frontend (port 3000):"
curl -f http://$EC2_IP:3000/ > /dev/null 2>&1 && echo "✅ Stats frontend accessible" || echo "❌ Stats frontend failed"

echo ""
echo "🔐 Testing authentication:"

# Test login API with proper headers
response=$(curl -s -X POST http://$EC2_IP:8001/api/login/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"email":"admin@example.com","password":"adminpass"}' \
  -w "%{http_code}")

echo "Login API response: $response"

# Test admin user directly in stats backend
echo ""
echo "🔍 Verifying admin user in stats backend:"
sudo docker-compose exec stats_backend python manage.py shell -c "
from stats.models import User
try:
    admin = User.objects.get(email='admin@example.com')
    print(f'✅ Found admin: {admin.email}')
    print(f'✅ Is admin: {admin.is_admin}')
    print(f'✅ Is staff: {admin.is_staff}')
    print(f'✅ Is active: {admin.is_active}')
    print(f'✅ Password check: {admin.check_password(\"adminpass\")}')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "🖼️  Testing media files:"
sudo docker-compose exec vacation_website ls -la /app/media/images/vacation_images/ | head -3

echo ""
echo "🌐 **FINAL RESULTS:**"
echo "   🏖️  Vacation Management: http://$EC2_IP:8000"
echo "   📊 Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "🔑 **Login Credentials:**"
echo "   Email: admin@example.com"
echo "   Password: adminpass"

# Check for any remaining errors
echo ""
echo "📋 Recent error logs:"
sudo docker-compose logs --tail=5 stats_backend 2>/dev/null || echo "No stats backend errors"