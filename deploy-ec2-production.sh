#!/bin/bash

# Production EC2 Deployment Script
# This script fixes both authentication and media serving issues

echo "🚀 Starting Production EC2 Deployment..."
echo "📅 $(date)"

# Set EC2 IP
EC2_IP="13.53.38.63"
echo "🌐 EC2 IP: $EC2_IP"

# Pull latest code and images
echo "📥 Pulling latest changes..."
cd FinalJBProject
git pull origin main

# Stop all running services
echo "🛑 Stopping all services..."
sudo docker-compose down -v

# Clean up everything for fresh start
echo "🧹 Complete cleanup..."
sudo docker system prune -af
sudo docker volume prune -f

# Pull latest Docker images from DockerHub
echo "📦 Pulling latest Docker images..."
sudo docker pull georgem94/vacation-website:latest
sudo docker pull georgem94/stats-backend:latest  
sudo docker pull georgem94/stats-frontend:latest
sudo docker pull postgres:15

# Update docker-compose.yml with correct EC2 IP
echo "📝 Configuring for EC2 IP: $EC2_IP..."
cp docker-compose.yml docker-compose.yml.backup

# Create updated docker-compose.yml with EC2 IP
cat > docker-compose.yml << EOF
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: vacation_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./vacation_website/VacationProjectGM/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  vacation_website:
    image: georgem94/vacation-website:latest
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DEBUG=1
      - DB_HOST=db
      - DB_NAME=vacation_db
      - DB_USER=postgres
      - DB_PASSWORD=password
      - DB_PORT=5432
    volumes:
      - ./vacation_website/VacationProjectGM/media:/app/media
    command: >
      sh -c "
      sleep 10 && 
      python manage.py migrate --run-syncdb && 
      python manage.py populate_db || true && 
      python manage.py runserver 0.0.0.0:8000"

  stats_backend:
    image: georgem94/stats-backend:latest
    ports:
      - "8001:8001"
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DEBUG=1
      - DB_HOST=db
      - DB_NAME=vacation_db
      - DB_USER=postgres
      - DB_PASSWORD=password
      - DB_PORT=5432
    command: >
      sh -c "
      sleep 15 && 
      python manage.py migrate --run-syncdb && 
      python manage.py runserver 0.0.0.0:8001"

  stats_frontend:
    image: georgem94/stats-frontend:latest
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://$EC2_IP:8001/api
      - REACT_APP_BACKEND_URL=http://$EC2_IP:8001
    depends_on:
      - stats_backend
      - vacation_website

volumes:
  postgres_data:
EOF

# Start database first
echo "📊 Starting PostgreSQL database..."
sudo docker-compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to initialize..."
sleep 40

# Verify database is ready
echo "🔍 Checking database health..."
sudo docker-compose exec db pg_isready -U postgres

# Start vacation website
echo "🏖️  Starting vacation website..."
sudo docker-compose up -d vacation_website

# Wait for vacation website to initialize
echo "⏳ Waiting for vacation website..."
sleep 30

# Create admin user in vacation system
echo "👤 Setting up admin user..."
sudo docker-compose exec vacation_website python manage.py shell -c "
from vacations.models import User, Role
from django.contrib.auth.hashers import make_password

print('Setting up admin user...')

# Ensure admin role exists
admin_role, created = Role.objects.get_or_create(role_name='admin')
print(f'Admin role: {admin_role} (new: {created})')

# Create/update admin user
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

# Always set password to ensure it works
admin_user.set_password('adminpass')
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.is_active = True
admin_user.role = admin_role
admin_user.save()

print(f'✅ Admin user ready: {admin_user.email}')
print(f'✅ Is admin: {admin_user.is_admin}')
print(f'✅ Password check: {admin_user.check_password(\"adminpass\")}')
"

# Start stats backend
echo "📈 Starting stats backend..."
sudo docker-compose up -d stats_backend

# Wait for stats backend
echo "⏳ Waiting for stats backend..."
sleep 25

# Verify admin user is accessible from stats backend
echo "🔍 Verifying admin user in stats backend..."
sudo docker-compose exec stats_backend python manage.py shell -c "
from stats.models import User
try:
    admin = User.objects.get(email='admin@example.com')
    print(f'✅ Admin found in stats: {admin.email}')
    print(f'✅ Is admin: {admin.is_admin}') 
    print(f'✅ Password works: {admin.check_password(\"adminpass\")}')
except User.DoesNotExist:
    print('❌ Admin user not found in stats backend')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Start stats frontend
echo "🎨 Starting stats frontend..."
sudo docker-compose up -d stats_frontend

# Wait for frontend to start
echo "⏳ Waiting for frontend..."
sleep 20

# Final verification
echo "📊 Final service status:"
sudo docker-compose ps

# Test API endpoints
echo ""
echo "🧪 Testing API endpoints..."
echo "Testing vacation website health:"
curl -f http://$EC2_IP:8000/ > /dev/null 2>&1 && echo "✅ Port 8000 accessible" || echo "❌ Port 8000 not accessible"

echo "Testing stats backend health:"
curl -f http://$EC2_IP:8001/api/ > /dev/null 2>&1 && echo "✅ Port 8001 accessible" || echo "❌ Port 8001 not accessible"

echo "Testing stats frontend health:"
curl -f http://$EC2_IP:3000/ > /dev/null 2>&1 && echo "✅ Port 3000 accessible" || echo "❌ Port 3000 not accessible"

# Test media files
echo ""
echo "🖼️  Testing media files:"
sudo docker-compose exec vacation_website ls -la /app/media/images/vacation_images/ | head -5

# Test login API directly
echo ""
echo "🔐 Testing login API directly:"
curl -X POST http://$EC2_IP:8001/api/login/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: test" \
  -d '{"email":"admin@example.com","password":"adminpass"}' \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "🔑 Login credentials for BOTH websites:"
echo "   Email: admin@example.com"
echo "   Password: adminpass"
echo ""
echo "🌐 Access URLs:"
echo "   🏖️  Vacation Management: http://$EC2_IP:8000"
echo "   📊 Statistics Dashboard: http://$EC2_IP:3000"
echo ""
echo "🔧 If issues persist, check logs with:"
echo "   sudo docker-compose logs stats_backend"
echo "   sudo docker-compose logs vacation_website"
echo "   sudo docker-compose logs stats_frontend"