#!/bin/bash

# Complete EC2 fix for both authentication and image loading
echo "🔧 Starting complete EC2 fix..."

# Get EC2 public IP
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "🌐 EC2 IP: $EC2_IP"

# Pull latest changes
cd FinalJBProject
git pull origin main

# Stop all services
echo "🛑 Stopping all services..."
sudo docker-compose down

# Remove volumes to start fresh
echo "🧹 Cleaning up volumes..."
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true

# Update docker-compose.yml to use EC2 IP for React frontend
echo "📝 Updating frontend configuration..."
sed -i "s|REACT_APP_API_URL=http://localhost:8001/api|REACT_APP_API_URL=http://$EC2_IP:8001/api|g" docker-compose.yml
sed -i "s|REACT_APP_BACKEND_URL=http://localhost:8001|REACT_APP_BACKEND_URL=http://$EC2_IP:8001|g" docker-compose.yml

# Start database first
echo "📊 Starting database..."
sudo docker-compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 30

# Check database health
sudo docker-compose exec db pg_isready -U postgres

# Start vacation website
echo "🏖️  Starting vacation website..."
sudo docker-compose up -d vacation_website

# Wait for vacation website to initialize
sleep 25

# Create admin user properly
echo "👤 Creating admin user..."
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User, Role
from django.contrib.auth.hashers import make_password

# Create admin role
admin_role, created = Role.objects.get_or_create(role_name='admin')
if created:
    print('✅ Created admin role')

# Create admin user
try:
    admin_user = User.objects.get(email='admin@example.com')
    admin_user.set_password('adminpass')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.role = admin_role
    admin_user.save()
    print('✅ Updated existing admin user')
except User.DoesNotExist:
    admin_user = User.objects.create_user(
        email='admin@example.com',
        password='adminpass',
        first_name='Admin',
        last_name='User',
        role=admin_role,
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    print('✅ Created new admin user')

print(f'Admin user ready: {admin_user.email}')
print(f'Is admin: {admin_user.is_admin}')
print(f'Is staff: {admin_user.is_staff}')
"

# Start stats backend
echo "📈 Starting stats backend..."
sudo docker-compose up -d stats_backend

sleep 20

# Start stats frontend
echo "🎨 Starting stats frontend..."
sudo docker-compose up -d stats_frontend

# Wait for all services
sleep 15

# Show service status
echo "📊 Service status:"
sudo docker-compose ps

# Test admin user in stats backend
echo "🔍 Testing admin user in stats backend..."
sudo docker-compose exec stats_backend python manage.py shell -c "
from stats.models import User
try:
    admin = User.objects.get(email='admin@example.com')
    print(f'✅ Admin found in stats: {admin.email}')
    print(f'Is admin: {admin.is_admin}')
    print(f'Is staff: {admin.is_staff}')
except User.DoesNotExist:
    print('❌ Admin user not found in stats backend')
"

echo ""
echo "✅ Complete fix applied!"
echo ""
echo "🔑 Login credentials for BOTH sites:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 Test URLs:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "🖼️  Images should now load at: http://$EC2_IP:8000/media/"