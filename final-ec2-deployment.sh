#!/bin/bash

# Final EC2 Deployment with Migration Fix
echo "🚀 Final EC2 Deployment with Migration Fix..."

EC2_IP="13.53.38.63"
cd FinalJBProject

# Pull latest code and updated Docker image
echo "📥 Pulling latest changes and Docker images..."
git pull origin main
sudo docker pull georgem94/stats-backend:latest

# Stop all services
echo "🛑 Stopping all services..."
sudo docker-compose down -v

# Clean everything for fresh start
echo "🧹 Complete cleanup..."
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true

# Start database
echo "📊 Starting database..."
sudo docker-compose up -d db

sleep 30

# Start vacation website (primary system)
echo "🏖️  Starting vacation website..."
sudo docker-compose up -d vacation_website

sleep 25

# Create admin user
echo "👤 Creating admin user..."
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User, Role

admin_role, created = Role.objects.get_or_create(role_name='admin')
admin_user, created = User.objects.get_or_create(
    email='admin@example.com',
    defaults={
        'first_name': 'Admin',
        'last_name': 'User',
        'role': admin_role,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    }
)

admin_user.set_password('adminpass')
admin_user.save()
print(f'✅ Admin user ready: {admin_user.email}')
"

# Start stats backend with updated image (has migration)
echo "📈 Starting stats backend with migration fix..."
sudo docker-compose up -d stats_backend

sleep 25

# Start stats frontend
echo "🎨 Starting stats frontend..."
sudo docker-compose up -d stats_frontend

sleep 15

# Final verification
echo ""
echo "📊 Service Status:"
sudo docker-compose ps

echo ""
echo "🧪 Testing All Systems:"

# Test vacation website
curl -f http://$EC2_IP:8000/ > /dev/null 2>&1 && echo "✅ Vacation website (8000) - Working" || echo "❌ Vacation website (8000) - Failed"

# Test stats backend
curl -f http://$EC2_IP:8001/api/ > /dev/null 2>&1 && echo "✅ Stats backend (8001) - Working" || echo "❌ Stats backend (8001) - Failed"

# Test stats frontend
curl -f http://$EC2_IP:3000/ > /dev/null 2>&1 && echo "✅ Stats frontend (3000) - Working" || echo "❌ Stats frontend (3000) - Failed"

# Test login API
echo ""
echo "🔐 Testing Login API:"
curl -X POST http://$EC2_IP:8001/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"adminpass"}' \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "🔑 Login credentials for BOTH sites:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 Test these URLs:"
echo "   🏖️  Vacation Management: http://$EC2_IP:8000"
echo "   📊 Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "📝 If issues persist, check logs:"
echo "   sudo docker-compose logs stats_backend"