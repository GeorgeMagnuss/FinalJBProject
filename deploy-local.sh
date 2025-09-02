#!/bin/bash
set -e

echo "🚀 Starting vacation website deployment (local)..."

# Create local docker-compose with different DB port
cat > docker-compose.local.yml << 'EOF'
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
      - "5433:5432"
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
    command: sh -c 'python manage.py migrate && python manage.py populate_db || true && python manage.py runserver 0.0.0.0:8000'

  stats_backend:
    image: georgem94/stats-backend:latest
    ports:
      - "8001:8001"
    depends_on:
      vacation_website:
        condition: service_started
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
      - ./stats_website/backend/stats:/app/stats
    command: sh -c 'python manage.py runserver 0.0.0.0:8001'

  stats_frontend:
    image: georgem94/stats-frontend:latest
    ports:
      - "3000:3000"
    depends_on:
      - stats_backend
      - vacation_website

volumes:
  postgres_data:
EOF

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose -f docker-compose.local.yml pull

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.local.yml down

# Start all services
echo "▶️ Starting all services..."
docker-compose -f docker-compose.local.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 15

# Check service health
echo "🔍 Checking service health..."
docker-compose -f docker-compose.local.yml ps

echo "✅ Local deployment complete!"
echo ""
echo "🌐 Services available at:"
echo "  - Main website: http://localhost:8000"
echo "  - Stats backend: http://localhost:8001"  
echo "  - Stats frontend: http://localhost:3000"
echo ""
echo "🔐 Admin credentials:"
echo "  - Email: admin@vacation.com"
echo "  - Password: admin123"