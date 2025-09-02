#!/bin/bash

# Verify admin password in stats_backend database
echo "🔍 Verifying admin password in stats_backend database..."

cd FinalJBProject

# Check if stats_backend is running
echo "📊 Checking stats_backend status..."
sudo docker-compose ps stats_backend

echo ""
echo "🔐 Testing admin password through stats_backend container..."

# Connect to stats_backend and test password
sudo docker-compose exec stats_backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

print('🔍 Checking admin user password...')
print('')

try:
    admin = User.objects.get(email='admin@example.com')
    
    print(f'✅ Found user: {admin.email}')
    print(f'   First name: {admin.first_name}')  
    print(f'   Last name: {admin.last_name}')
    print(f'   Is active: {admin.is_active}')
    print(f'   Is staff: {admin.is_staff}')
    print(f'   Is admin: {admin.is_admin}')
    print('')
    
    # Test the exact password
    password_result = admin.check_password('adminpass')
    print(f'🔑 Password check for \"adminpass\": {password_result}')
    
    if password_result:
        print('✅ PASSWORD IS CORRECT - Authentication logic issue')
        print('')
        print('🔍 Testing authentication backend directly...')
        from stats.backends import EmailBackend
        backend = EmailBackend()
        auth_result = backend.authenticate(None, username='admin@example.com', password='adminpass')
        print(f'Backend authenticate result: {auth_result}')
    else:
        print('❌ PASSWORD IS INCORRECT - Database issue')
        print('')
        print('🔄 Setting correct password...')
        admin.set_password('adminpass')
        admin.save()
        
        # Test again
        recheck = admin.check_password('adminpass')
        print(f'After reset - Password check: {recheck}')
        
except User.DoesNotExist:
    print('❌ Admin user does not exist!')
except Exception as e:
    print(f'❌ Error: {e}')
"