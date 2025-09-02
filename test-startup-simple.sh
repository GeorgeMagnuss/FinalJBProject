#!/bin/bash

# Test vacation website startup with environment debugging
echo "🔍 Testing vacation website startup with environment debugging..."

cd FinalJBProject

# Stop all services
sudo docker-compose down

# Start database
sudo docker-compose up -d db
sleep 30

# Test the vacation website container startup by overriding command entirely
echo ""
echo "🏖️  Testing with custom command..."
sudo docker run --rm \
  --network finaljbproject_default \
  -p 8000:8000 \
  -e DEBUG=1 \
  -e DB_HOST=db \
  -e DB_NAME=vacation_db \
  -e DB_USER=postgres \
  -e DB_PASSWORD=password \
  -e DB_PORT=5432 \
  georgem94/vacation-website:latest \
  sh -c "
    echo 'Environment variables:' &&
    echo 'DB_HOST=' \$DB_HOST &&
    echo 'DB_USER=' \$DB_USER &&
    echo 'DB_PASSWORD=' \$DB_PASSWORD &&
    echo 'DB_PORT=' \$DB_PORT &&
    echo 'DB_NAME=' \$DB_NAME &&
    echo 'Starting Django directly...' &&
    python manage.py migrate --run-syncdb &&
    python manage.py populate_db || echo 'DB populate failed/skipped' &&
    echo 'Starting server on 0.0.0.0:8000...' &&
    python manage.py runserver 0.0.0.0:8000
  "

# This should show us what's happening in the container