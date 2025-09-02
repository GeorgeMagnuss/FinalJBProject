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

### Run with Docker Compose

```bash
docker-compose up --build
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

## Notes for AWS EC2 Deployment

1. Upload Docker images to Docker Hub
2. Pull and run with Docker Compose on EC2
3. Configure security groups for ports 3000 and 8000
4. Access via EC2 public IP:
   - Vacation site: `http://<EC2_IP>:8000`
   - Statistics site: `http://<EC2_IP>:3000`