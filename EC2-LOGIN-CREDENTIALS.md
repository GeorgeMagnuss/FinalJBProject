# AWS EC2 Login Credentials

## For Port 8000 (Vacation Management):
- **Email:** `admin@example.com`
- **Password:** `adminpass`

## For Port 3000 (Statistics Dashboard):
- **Email:** `admin@example.com` 
- **Password:** `adminpass`

## Database Details:
- **PostgreSQL:** localhost:5432
- **Database:** vacation_db
- **Username:** postgres
- **Password:** password

## Troubleshooting:
If login fails, run the database initialization script:
```bash
cd FinalJBProject
chmod +x init-database-ec2.sh
./init-database-ec2.sh
```

## Service URLs:
- Vacation Management: http://YOUR_EC2_IP:8000
- Statistics Dashboard: http://YOUR_EC2_IP:3000
- Stats API: http://YOUR_EC2_IP:8001/api/