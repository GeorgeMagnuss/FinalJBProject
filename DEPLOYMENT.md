# AWS EC2 Deployment Instructions

## Prerequisites
1. AWS EC2 instance with Docker and Docker Compose installed
2. Security groups configured for ports 3000, 8000, 8001, and 5432
3. Docker Hub account for pushing images

## Option 1: Deploy Both Applications Together

```bash
# Clone the repository
git clone <your-repo-url>
cd FinalVacationProjectJBSept2

# Run complete system
docker-compose up --build -d
```

Access:
- Vacation Website: `http://<EC2_IP>:8000`
- Statistics Website: `http://<EC2_IP>:3000`

## Option 2: Deploy Applications Separately

### Deploy Vacation Website Only

```bash
cd vacation_website
docker-compose up --build -d
```

Access: `http://<EC2_IP>:8000`

### Deploy Statistics Website Only

```bash
cd stats_website
docker-compose up --build -d
```

Access: `http://<EC2_IP>:3000`

## Docker Hub Deployment

### Push Images to Docker Hub

```bash
# Build and tag images
docker build -t <username>/vacation-website:latest ./vacation_website
docker build -t <username>/stats-backend:latest ./stats_website/backend
docker build -t <username>/stats-frontend:latest ./stats_website/frontend

# Push to Docker Hub
docker push <username>/vacation-website:latest
docker push <username>/stats-backend:latest
docker push <username>/stats-frontend:latest
```

### Pull and Run on EC2

```bash
# Pull images
docker pull <username>/vacation-website:latest
docker pull <username>/stats-backend:latest
docker pull <username>/stats-frontend:latest

# Use the docker-compose files with image references instead of build contexts
```

## Environment Variables for Production

Set these environment variables on EC2:

```bash
export DEBUG=0
export DB_HOST=db
export DB_NAME=vacation_db
export DB_USER=postgres
export DB_PASSWORD=your_secure_password
export ALLOWED_HOSTS=*
```

## Security Notes for Production

1. Change default passwords
2. Use environment variables for sensitive data
3. Configure proper firewall rules
4. Use HTTPS in production
5. Set DEBUG=0 for production

## Testing the Deployment

1. Check if containers are running: `docker-compose ps`
2. View logs: `docker-compose logs`
3. Test database connection: `docker-compose exec db psql -U postgres -d vacation_db`