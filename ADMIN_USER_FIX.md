# Admin User Authentication Fix

## Problem
The stats website backend expects `admin@vacation.com` with password `admin123`, but the vacation website's `populate_db` command was creating `admin@example.com` with password `adminpass`, causing login failures.

## Solution Applied
Updated the `populate_db.py` file to create the correct admin user credentials:
- Email: `admin@vacation.com` 
- Password: `admin123`

## Files Modified
- `/vacation_website/vacations/management/commands/populate_db.py`

## Changes Made
```diff
- email='admin@example.com',
+ email='admin@vacation.com',
...
- admin_user.set_password('adminpass')
+ admin_user.set_password('admin123')
```

## How to Deploy
1. Deploy the updated code to your EC2 instance
2. Restart the containers with `docker-compose down && docker-compose up -d`
3. The populate_db command will run automatically and create/update the admin user

## How to Revert
If the changes cause issues, you can revert using one of these methods:

### Method 1: Use the revert script
```bash
./revert_populate_db.sh
```

### Method 2: Manual revert
```bash
cp vacation_website/vacations/management/commands/populate_db.py.backup vacation_website/vacations/management/commands/populate_db.py
```

### Method 3: If you need to create the old admin user
Connect to the Django shell in the vacation_website container:
```bash
docker-compose exec vacation_website python manage.py shell
```

Then run:
```python
from vacations.models import User, Role
admin_role = Role.objects.get(role_name='admin')
admin_user = User.objects.create(
    email='admin@example.com',
    first_name='Admin',
    last_name='User',
    role=admin_role,
    is_staff=True,
    is_superuser=True
)
admin_user.set_password('adminpass')
admin_user.save()
```

## Backup Location
- Original file backed up to: `vacation_website/vacations/management/commands/populate_db.py.backup`

## Important Notes
- The `populate_db` command uses `get_or_create()`, so it won't overwrite existing users
- If you already have users in the database, you may need to manually update or create the admin@vacation.com user
- The stats backend has hardcoded credentials check in `/stats_website/backend/stats/views.py` (line 55-56)