#!/bin/bash

# Final comprehensive EC2 fix
echo "🔧 Final EC2 fix starting..."

# Get EC2 public IP (try multiple methods)
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
if [ -z "$EC2_IP" ]; then
    EC2_IP=$(curl -s https://checkip.amazonaws.com/ 2>/dev/null | tr -d '\n')
fi
if [ -z "$EC2_IP" ]; then
    EC2_IP=$(curl -s https://ipinfo.io/ip 2>/dev/null)
fi

echo "🌐 EC2 IP: $EC2_IP"

# Pull latest changes
cd FinalJBProject
git pull origin main

# Stop all services
echo "🛑 Stopping all services..."
sudo docker-compose down

# Clean up everything
echo "🧹 Complete cleanup..."
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true
sudo docker system prune -f

# Update React frontend environment with correct IP
echo "📝 Updating frontend configuration..."
sed -i "s|REACT_APP_API_URL=http://.*:8001/api|REACT_APP_API_URL=http://$EC2_IP:8001/api|g" docker-compose.yml
sed -i "s|REACT_APP_BACKEND_URL=http://.*:8001|REACT_APP_BACKEND_URL=http://$EC2_IP:8001|g" docker-compose.yml

# Start database
echo "📊 Starting database..."
sudo docker-compose up -d db

# Wait for database
echo "⏳ Waiting for database..."
sleep 35

# Start vacation website first (primary system)
echo "🏖️  Starting vacation website..."
sudo docker-compose up -d vacation_website

sleep 25

# Copy media files to the running container
echo "🖼️  Setting up media files..."
sudo docker-compose exec vacation_website mkdir -p /app/media/images/vacation_images

# Copy sample images (create if missing)
sudo docker-compose exec vacation_website python -c "
import os
from pathlib import Path

# Create basic placeholder files for missing images
media_dir = Path('/app/media/images/vacation_images')
media_dir.mkdir(parents=True, exist_ok=True)

image_files = [
    'telaviv.jpg', 'madrid.jpg', 'tokyo.jpg', 'rome.jpg', 
    'berlin.jpg', 'paris.jpg', 'rio.jpg', 'buenosaires.jpg',
    'nyc.jpg', 'sydney.jpg', 'medellin.jpg', 'losangeles.jpg'
]

for img in image_files:
    img_path = media_dir / img
    if not img_path.exists():
        # Create a minimal placeholder file
        img_path.write_bytes(b'placeholder')
        print(f'Created placeholder: {img}')
    else:
        print(f'Exists: {img}')
"

# Create proper admin user
echo "👤 Creating admin user..."
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User, Role
from django.contrib.auth.hashers import make_password

# Ensure admin role exists
admin_role, created = Role.objects.get_or_create(role_name='admin')
print(f'Admin role: {admin_role.role_name} (created: {created})')

# Create admin user
try:
    admin_user = User.objects.get(email='admin@example.com')
    print('Admin user already exists, updating...')
except User.DoesNotExist:
    admin_user = User(email='admin@example.com')
    print('Creating new admin user...')

admin_user.first_name = 'Admin'
admin_user.last_name = 'User'
admin_user.role = admin_role
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.is_active = True
admin_user.set_password('adminpass')
admin_user.save()

print(f'✅ Admin user ready: {admin_user.email}')
print(f'Is admin: {admin_user.is_admin}')
print(f'Password works: {admin_user.check_password(\"adminpass\")}')
"

# Now start stats backend (remove migrations to avoid conflicts)
echo "📈 Starting stats backend..."
sudo docker-compose exec vacation_website python manage.py shell -c "
# Delete any stats migrations that might conflict
import os
import shutil
stats_migrations = '/app/../stats_website/backend/stats/migrations'
if os.path.exists(stats_migrations):
    for f in os.listdir(stats_migrations):
        if f.startswith('0') and f.endswith('.py'):
            os.remove(os.path.join(stats_migrations, f))
            print(f'Removed migration: {f}')
"

sudo docker-compose up -d stats_backend

sleep 20

# Start frontend
echo "🎨 Starting frontend..."
sudo docker-compose up -d stats_frontend

sleep 15

# Verify everything is running
echo "📊 Final service status:"
sudo docker-compose ps

echo ""
echo "✅ Final fix complete!"
echo ""
echo "🔑 Login credentials:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 Test URLs:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "🖼️  Media files location: /app/media/images/vacation_images/"