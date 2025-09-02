#!/bin/bash

# EC2 fix with known IP
EC2_IP="13.53.38.63"
echo "🌐 Using EC2 IP: $EC2_IP"

# Pull latest changes
cd FinalJBProject
git pull origin main

# Stop all services
echo "🛑 Stopping all services..."
sudo docker-compose down

# Clean up volumes
echo "🧹 Cleaning volumes..."
sudo docker volume rm finaljbproject_postgres_data 2>/dev/null || true

# Update React frontend with correct IP
echo "📝 Updating frontend configuration with IP $EC2_IP..."
sed -i "s|REACT_APP_API_URL=http://.*:8001/api|REACT_APP_API_URL=http://$EC2_IP:8001/api|g" docker-compose.yml
sed -i "s|REACT_APP_BACKEND_URL=http://.*:8001|REACT_APP_BACKEND_URL=http://$EC2_IP:8001|g" docker-compose.yml

# Start database
echo "📊 Starting database..."
sudo docker-compose up -d db

# Wait for database
sleep 30

# Start vacation website
echo "🏖️  Starting vacation website..."
sudo docker-compose up -d vacation_website

sleep 25

# Create media files
echo "🖼️  Setting up media files..."
sudo docker-compose exec vacation_website bash -c "
mkdir -p /app/media/images/vacation_images
cd /app/media/images/vacation_images

# Create placeholder image files
echo 'Creating image placeholders...'
for img in telaviv.jpg madrid.jpg tokyo.jpg rome.jpg berlin.jpg paris.jpg rio.jpg buenosaires.jpg nyc.jpg sydney.jpg medellin.jpg losangeles.jpg; do
    echo 'PLACEHOLDER' > \$img
    echo \"Created \$img\"
done

ls -la
"

# Create admin user
echo "👤 Creating admin user..."
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User, Role

# Create admin role
admin_role, created = Role.objects.get_or_create(role_name='admin')

# Create/update admin user
try:
    admin_user = User.objects.get(email='admin@example.com')
except User.DoesNotExist:
    admin_user = User(email='admin@example.com')

admin_user.first_name = 'Admin'
admin_user.last_name = 'User'
admin_user.role = admin_role
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.is_active = True
admin_user.set_password('adminpass')
admin_user.save()

print(f'✅ Admin user: {admin_user.email}')
print(f'Password check: {admin_user.check_password(\"adminpass\")}')
"

# Start stats backend (without migrations to avoid conflicts)
echo "📈 Starting stats backend..."
sudo docker-compose run --rm stats_backend python manage.py shell -c "
# Just verify the admin user exists in this context
from stats.models import User
admin = User.objects.get(email='admin@example.com')
print(f'✅ Stats can see admin: {admin.email}')
"

sudo docker-compose up -d stats_backend

sleep 20

# Start frontend with correct IP
echo "🎨 Starting frontend..."
sudo docker-compose up -d stats_frontend

sleep 15

echo ""
echo "✅ Fix complete!"
echo ""
echo "🔑 Login credentials:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 Test URLs:"
echo "   Vacation Management: http://$EC2_IP:8000"
echo "   Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "📊 Service status:"
sudo docker-compose ps