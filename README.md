# Vacation Management System
**Python Full Stack Web Developer - Course Project Part III**

**Student:** George Mattar

A comprehensive vacation management system with real-time statistics dashboard, built using modern web technologies and deployed on AWS Cloud.

## Quick Start

```bash
docker-compose up
```

**Access Points:**
- **Vacation Management:** http://localhost:8000
- **Statistics Dashboard:** http://localhost:3000

**Admin Credentials:** admin@vacation.com / admin123

## Project Overview

This system consists of two integrated applications:

### 1. Vacation Management Website (Django)
- User registration and authentication
- Browse and search vacation packages
- Like/unlike destinations
- Admin panel for vacation management
- Image gallery with destination photos

### 2. Statistics Dashboard (React + Django API)
- Admin-only access to system analytics
- Real-time vacation statistics (past/ongoing/future)
- User engagement metrics
- Interactive likes distribution with visual charts
- Auto-refresh capabilities

## Technical Architecture

### Backend
- **Django REST Framework** for statistics API
- **PostgreSQL** database shared between services
- **CORS enabled** for cross-service communication
- **Session-based authentication**

### Frontend  
- **React with TypeScript** for statistics dashboard
- **Django templates** for vacation website
- **Responsive design** with modern CSS
- **Real-time data updates**

### Infrastructure
- **Docker Compose** orchestration
- **Multi-container deployment**
- **PostgreSQL database** with automatic initialization
- **AWS EC2** cloud deployment

## API Endpoints

### Statistics API (`http://localhost:8001/api/`)
- `POST /login/` - Admin authentication
- `POST /logout/` - Session termination  
- `GET /stats/vacations/` - Vacation timeline statistics
- `GET /total/users/` - Total registered users
- `GET /total/likes/` - Total user likes
- `GET /distribution/likes/` - Likes by destination

### Example API Responses
```json
// /stats/vacations/
{"pastVacations": 12, "ongoingVacations": 7, "futureVacations": 15}

// /total/users/  
{"totalUsers": 37}

// /distribution/likes/
[{"destination": "Rome", "likes": 3}, {"destination": "Rhodes", "likes": 8}]
```

## Database Schema

**Core Tables:**
- `roles` - User access levels (admin/user)
- `users` - Account management with role assignments
- `countries` - Destination reference data
- `vacations` - Travel packages with dates and descriptions
- `likes` - User preferences tracking

## Docker Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `db` | `postgres:15` | 5432 | PostgreSQL database |
| `vacation_website` | `georgem94/vacation-website:latest` | 8000 | Django vacation app |
| `stats_backend` | `georgem94/stats-backend:latest` | 8001 | Statistics API |
| `stats_frontend` | `georgem94/stats-frontend:latest` | 3000 | React dashboard |

## Development Features

### Security
- Environment variables for configuration
- Admin-only access to statistics
- CORS protection between services
- Input validation and SQL injection prevention

### User Experience
- Intuitive navigation between applications
- Real-time data updates without page refresh
- Error handling with user-friendly messages
- Mobile-responsive design

### Code Quality
- Clean code with proper naming conventions
- Separated concerns across services
- Comprehensive error handling
- Type hints and documentation

## Environment Configuration

Sample environment variables are provided in `.env.sample` files for reference. The production deployment uses environment variables configured directly in `docker-compose.yml`.

## Course Compliance

This project fulfills all Course Project Part III requirements:
- ✅ PostgreSQL database integration
- ✅ Django backend with required API routes
- ✅ React frontend with statistics visualization
- ✅ Docker containerization and composition
- ✅ AWS Cloud deployment capability