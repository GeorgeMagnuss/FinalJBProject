#!/bin/bash

# Fix admin login issues on EC2
echo "🔧 Fixing admin login issues..."

# Pull latest changes
cd FinalJBProject
git pull origin main

# Stop services
sudo docker-compose down

# Clean up and restart
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true

# Start database first
echo "📊 Starting database..."
sudo docker-compose up -d db

# Wait for database
sleep 30

# Start vacation website and create admin user
echo "🏖️  Starting vacation website..."
sudo docker-compose up -d vacation_website

sleep 20

# Create proper admin user
echo "👤 Creating admin user..."
sudo docker-compose exec vacation_website python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacation_project.settings')
django.setup()
from vacations.models import User, Role
from django.contrib.auth.hashers import make_password

# Get or create admin role
admin_role, created = Role.objects.get_or_create(role_name='admin')

# Create or update admin user  
admin_user, created = User.objects.get_or_create(
    email='admin@example.com',
    defaults={
        'first_name': 'Admin',
        'last_name': 'User', 
        'role': admin_role,
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
        'password': make_password('adminpass')
    }
)

if not created:
    admin_user.set_password('adminpass')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.role = admin_role
    admin_user.save()

print('✅ Admin user ready:', admin_user.email)
"

# Start all services
echo "🚀 Starting all services..."
sudo docker-compose up -d

sleep 15

# Show service status
sudo docker-compose ps

EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo ""
echo "✅ Fix complete!"
echo ""
echo "🔑 Login credentials for BOTH sites:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 Test URLs:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"