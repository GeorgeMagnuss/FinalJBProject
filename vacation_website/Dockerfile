FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements from the correct location
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create wait script
RUN echo '#!/bin/bash\n\
set -e\n\
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n\
  echo "Waiting for database..."\n\
  sleep 2\n\
done\n\
echo "Database is ready!"\n\
python manage.py migrate\n\
python manage.py populate_db\n\
python manage.py runserver 0.0.0.0:8000' > /app/wait-for-db.sh && \
chmod +x /app/wait-for-db.sh

EXPOSE 8000

CMD ["/app/wait-for-db.sh"]