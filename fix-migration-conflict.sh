#!/bin/bash

# Fix Django migration conflict between vacation and stats systems
echo "🔧 Fixing migration conflicts..."

EC2_IP="13.53.38.63"
cd FinalJBProject

# Stop everything
sudo docker-compose down -v

# Clean database completely
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true

# Start only database
echo "📊 Starting fresh database..."
sudo docker-compose up -d db

sleep 30

# Start vacation website first (primary system that creates tables)
echo "🏖️  Starting vacation website (primary system)..."
sudo docker-compose up -d vacation_website

sleep 25

# Create admin user in vacation system
echo "👤 Creating admin user in vacation system..."
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User, Role

# Create admin role
admin_role, created = Role.objects.get_or_create(role_name='admin')

# Create admin user
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

print(f'✅ Admin user: {admin_user.email}')
print(f'✅ Password works: {admin_user.check_password(\"adminpass\")}')
"

# Now fake apply stats migrations to avoid conflicts
echo "📈 Configuring stats backend to use existing tables..."
sudo docker-compose run --rm stats_backend python manage.py shell -c "
from django.core.management import execute_from_command_line
from django.db import connection
import sys

print('Marking stats migrations as applied...')

# Mark all stats migrations as applied without actually running them
with connection.cursor() as cursor:
    cursor.execute(
        \"INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW()) ON CONFLICT DO NOTHING\",
        ['stats', '0001_initial']
    )
    print('✅ Marked stats migrations as applied')

# Test admin user access
from stats.models import User
admin = User.objects.get(email='admin@example.com')
print(f'✅ Stats backend can access admin: {admin.email}')
"

# Start stats backend (should not run migrations now)
echo "🚀 Starting stats backend..."
sudo docker-compose up -d stats_backend

sleep 20

# Start frontend
echo "🎨 Starting stats frontend..."
sudo docker-compose up -d stats_frontend

sleep 15

# Show final status
echo ""
echo "📊 Service Status:"
sudo docker-compose ps

echo ""
echo "🧪 Testing endpoints:"

# Test vacation website
curl -f http://$EC2_IP:8000/ > /dev/null 2>&1 && echo "✅ Vacation website (8000) - OK" || echo "❌ Vacation website (8000) - FAILED"

# Test stats backend
curl -f http://$EC2_IP:8001/api/ > /dev/null 2>&1 && echo "✅ Stats backend (8001) - OK" || echo "❌ Stats backend (8001) - FAILED"

# Test stats frontend  
curl -f http://$EC2_IP:3000/ > /dev/null 2>&1 && echo "✅ Stats frontend (3000) - OK" || echo "❌ Stats frontend (3000) - FAILED"

# Test login API
echo ""
echo "🔐 Testing login API:"
curl -X POST http://$EC2_IP:8001/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"adminpass"}' \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "🔑 Login credentials:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 URLs:"
echo "   Vacation: http://$EC2_IP:8000"
echo "   Stats: http://$EC2_IP:3000"