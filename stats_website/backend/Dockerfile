FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .
# Remove all migration files since we use unmanaged models
RUN find . -path "*/migrations/*.py" -delete 2>/dev/null || true
RUN find . -path "*/migrations/*.pyc" -delete 2>/dev/null || true

# Create wait script
RUN echo '#!/bin/bash\n\
set -e\n\
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n\
  echo "Waiting for database..."\n\
  sleep 2\n\
done\n\
echo "Database is ready!"\n\
echo "Skipping migrations - using unmanaged models pointing to existing tables"\n\
python manage.py runserver 0.0.0.0:8001' > /app/wait-for-db.sh && \
chmod +x /app/wait-for-db.sh

EXPOSE 8001

CMD ["/app/wait-for-db.sh"]