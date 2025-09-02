#!/bin/bash

# Check admin password in stats_backend container
echo "🔍 Checking admin password in stats_backend..."

cd FinalJBProject

# Connect to stats_backend container and check admin password
sudo docker-compose exec stats_backend python manage.py shell -c "
from stats.models import User

print('🔍 Checking admin user password...')
print('')

try:
    # Get the admin user
    admin_user = User.objects.get(email='admin@example.com')
    
    print(f'✅ Found user: {admin_user.email}')
    print(f'First name: {admin_user.first_name}')
    print(f'Last name: {admin_user.last_name}')
    print(f'Is active: {admin_user.is_active}')
    print(f'Is staff: {admin_user.is_staff}')
    print(f'Is superuser: {admin_user.is_superuser}')
    print(f'Is admin: {admin_user.is_admin}')
    print('')
    
    # Check password
    password_check = admin_user.check_password('adminpass')
    print(f'🔑 Password check for \"adminpass\": {password_check}')
    
    if password_check:
        print('✅ Password is CORRECT')
    else:
        print('❌ Password is INCORRECT')
        print('')
        print('Setting correct password...')
        admin_user.set_password('adminpass')
        admin_user.save()
        
        # Verify the fix
        new_check = admin_user.check_password('adminpass')
        print(f'🔄 After reset - Password check: {new_check}')
    
except User.DoesNotExist:
    print('❌ Admin user does not exist!')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "🔗 If password was reset, try logging in again at:"
echo "   http://13.53.38.63:3000"