# EC2 Deployment Fix Guide

## The Problem
When accessing http://13.53.38.63:3000/statistics, you get "Failed to fetch statistics data" because:
- The stats frontend (port 3000) tries to connect to the stats backend API (port 8001)
- Port 8001 is NOT open in your EC2 security group
- Without access to port 8001, the frontend cannot fetch data

## Solution: Open Port 8001 in AWS Security Group

1. **Go to AWS Console**
   - Navigate to EC2 → Instances
   - Find your instance (13.53.38.63)
   - Click on the Security tab
   - Click on the Security Group link

2. **Add Inbound Rule**
   - Click "Edit inbound rules"
   - Click "Add rule"
   - Configure:
     - Type: `Custom TCP`
     - Port range: `8001`
     - Source: `0.0.0.0/0` (or restrict to your IP for better security)
   - Click "Save rules"

3. **Verify All Required Ports**
   Your security group should have these inbound rules:
   - Port 22 (SSH)
   - Port 8000 (Vacation website)
   - Port 8001 (Stats API backend) ← **THIS IS MISSING**
   - Port 3000 (Stats frontend)

## Testing After Fix

1. Test the API directly:
   ```bash
   curl http://13.53.38.63:8001/api/login/ -X POST \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@vacation.com","password":"admin123"}'
   ```
   
   Should return: `{"success": true, "message": "Login successful"}`

2. Access the stats dashboard:
   - Go to http://13.53.38.63:3000
   - Login with admin@vacation.com / admin123
   - Statistics should load successfully

## Alternative Solution (Without Opening Port 8001)

If you cannot open port 8001, you'll need to use a reverse proxy setup with nginx to route all traffic through port 80. Contact me if you need this solution implemented.