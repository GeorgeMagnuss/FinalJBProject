# Deployment Instructions for AWS EC2

## Prerequisites
- AWS EC2 instance is running
- SSH access to the EC2 instance
- Docker and Docker Compose are installed on the EC2 instance

## Step-by-Step Deployment

### 1. SSH into your EC2 instance
```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

### 2. Navigate to your project directory or clone it
If the project is already on the server:
```bash
cd /path/to/FinalVacationProjectJBSept2
```

If you need to clone it:
```bash
git clone https://github.com/GeorgeMagnuss/FinalJBProject.git FinalVacationProjectJBSept2
cd FinalVacationProjectJBSept2
```

### 3. Pull the latest changes
```bash
git pull origin main
```

### 4. Stop and remove existing containers and volumes
**IMPORTANT**: This will delete all data including the database. Make sure to backup if needed.
```bash
docker-compose down -v
```

### 5. Pull the latest Docker images
```bash
docker-compose pull
```

### 6. Start the services
```bash
docker-compose up -d
```

### 7. Verify services are running
```bash
docker-compose ps
```

You should see all 4 services running:
- db (PostgreSQL)
- vacation_website
- stats_backend  
- stats_frontend

### 8. Check the logs to ensure admin user was created
```bash
docker-compose logs vacation_website | grep "admin@vacation.com"
```

You should see: `Created admin user: admin@vacation.com`

### 9. Test the application
- Vacation Website: http://your-ec2-ip:8000
- Stats Dashboard: http://your-ec2-ip:3000

### 10. Login credentials
- Email: `admin@vacation.com`
- Password: `admin123`

## What Changed?
1. Updated `populate_db.py` to create admin user with correct credentials
2. Docker image `georgem94/vacation-website:latest` has been updated on Docker Hub
3. The stats backend expects these specific credentials (hardcoded check)

## Troubleshooting

### If login still fails:
1. Check if the database was properly initialized:
```bash
docker-compose exec vacation_website python manage.py shell
```

Then in the Python shell:
```python
from vacations.models import User
User.objects.filter(email='admin@vacation.com').exists()
```

2. Manually create the admin user if needed:
```bash
docker-compose exec vacation_website python manage.py shell
```

```python
from vacations.models import User, Role
admin_role = Role.objects.get(role_name='admin')
admin_user = User.objects.create(
    email='admin@vacation.com',
    first_name='Admin',
    last_name='User', 
    role=admin_role,
    is_staff=True,
    is_superuser=True
)
admin_user.set_password('admin123')
admin_user.save()
```

### To revert the changes:
If you need to go back to the original setup:
```bash
./revert_populate_db.sh
docker-compose build vacation_website
docker-compose up -d
```

## Security Notes
- The hardcoded credentials in stats backend (line 55-56 in stats/views.py) should be replaced with proper authentication in production
- Consider using environment variables for sensitive credentials
- Use HTTPS in production

## Monitoring
Check application logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f stats_backend
```

## Backup Reminder
Before any deployment:
```bash
# Backup the database
docker-compose exec db pg_dump -U postgres vacation_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Support
If issues persist, check:
1. `ADMIN_USER_FIX.md` for detailed explanation of the fix
2. GitHub repository: https://github.com/GeorgeMagnuss/FinalJBProject
3. Docker Hub images:
   - georgem94/vacation-website:latest
   - georgem94/stats-backend:latest
   - georgem94/stats-frontend:latest