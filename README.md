# Vacation Management System - Complete Project

**Student Name:** George Mattar

This is the complete vacation management system consisting of two main applications:
1. **Vacation Website** - Main vacation management application
2. **Statistics Website** - Admin statistics dashboard

## Project Structure

```
projectRoot/
├── vacation_website/          ← Part 2 project (vacation management)
│   ├── Dockerfile
│   ├── initial_data.json
│   ├── init_db.sql
│   └── ... (Django project files)
├── stats_website/
│   ├── backend/              ← Stats API server
│   │   ├── Dockerfile
│   │   └── ... (Django project files)
│   ├── frontend/             ← Stats React client
│   │   ├── Dockerfile
│   │   └── ... (React project files)
└── docker-compose.yml
```

## Technologies Used

- **Database:** PostgreSQL
- **Backend:** Django (Python)
- **Frontend:** React (TypeScript)
- **Containerization:** Docker & Docker Compose
- **Cloud Deployment:** AWS EC2

## How to Run the Complete Project

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000, 8000, 8001, and 5432 available

### Local Development

**Run these two commands in order:**
```bash
docker-compose pull
docker-compose up -d
```

This will start all services:
- **Database:** PostgreSQL on port 5432  
- **Vacation Website:** http://localhost:8000
- **Stats Backend API:** http://localhost:8001
- **Stats Frontend:** http://localhost:3000

### Default Admin Credentials
- **Email:** admin@vacation.com
- **Password:** admin123

### Access Points
- **Vacation Management:** http://localhost:8000
- **Statistics Dashboard:** http://localhost:3000

## API Endpoints (Stats Backend)

- `POST /api/login/` - Admin login
- `POST /api/logout/` - Logout
- `GET /api/stats/vacations/` - Vacation statistics
- `GET /api/total/users/` - Total users count
- `GET /api/total/likes/` - Total likes count
- `GET /api/distribution/likes/` - Likes distribution by destination

## Database Schema

The system uses a shared PostgreSQL database with the following tables:
- `roles` - User roles (admin/user)
- `users` - System users
- `countries` - Vacation destinations
- `vacations` - Vacation packages
- `likes` - User likes for vacations

## Production Deployment (AWS EC2)

### Prerequisites
- EC2 instance with Docker and Docker Compose installed
- Security groups configured for ports 3000, 8000, 8001, and 5432

### Manual Deployment Instructions

1. **Upload docker-compose.yml to your server:**
   ```bash
   scp -i your-key.pem docker-compose.yml ubuntu@<EC2_IP>:~/
   ```

2. **Connect to your server and run these two commands:**
   ```bash
   ssh -i your-key.pem ubuntu@<EC2_IP>
   ```
   
   **Run exactly these two commands in order:**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

3. **Access Applications:**
   - **Vacation Management:** `http://<EC2_IP>:8000`
   - **Statistics Dashboard:** `http://<EC2_IP>:3000`

### Docker Images
Pre-built multi-platform images available on Docker Hub:
- `georgem94/vacation-website:latest`
- `georgem94/stats-backend:latest`  
- `georgem94/stats-frontend:latest`

## Project Features

### Vacation Website (Port 8000)
- Browse vacation packages
- User registration and authentication
- Like/unlike vacation packages
- Admin panel for managing vacations

### Statistics Dashboard (Port 3000)
- Admin-only access
- Real-time vacation statistics
- User engagement metrics
- Likes distribution analysis

## Resolved Issues

✅ **Database Migration Conflicts** - Implemented unmanaged models for stats backend  
✅ **Frontend API Communication** - Fixed URL routing with `/api/` prefix  
✅ **Authentication Failures** - Corrected admin user password and role relationships  
✅ **Docker Multi-platform Support** - Built for both AMD64 and ARM64 architectures  
✅ **Production Configuration** - Environment-specific API URLs and CORS settings