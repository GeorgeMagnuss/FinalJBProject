#!/usr/bin/env python3

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacation_project.settings')
sys.path.append('/Users/george/Desktop/secondproject/VacationProjectGM')

django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from vacations.models import User, Role

def test_authentication():
    print("Testing login functionality...")
    
    # Test 1: Check users exist
    print("\nChecking users:")
    try:
        admin = User.objects.get(email='admin@example.com')
        user = User.objects.get(email='user@example.com')
        print(f"   ✓ Admin user found: {admin.email} (Role: {admin.role.role_name})")
        print(f"   ✓ Regular user found: {user.email} (Role: {user.role.role_name})")
    except User.DoesNotExist as e:
        print(f"   ✗ User not found: {e}")
        return False
    
    # Test 2: Check password validation
    print("\nTesting passwords:")
    admin_pwd_valid = admin.check_password('adminpass')
    user_pwd_valid = user.check_password('userpass')
    print(f"   Admin password valid: {'✓' if admin_pwd_valid else '✗'}")
    print(f"   User password valid: {'✓' if user_pwd_valid else '✗'}")
    
    if not (admin_pwd_valid and user_pwd_valid):
        return False
    
    # Test 3: Test authentication backend
    print("\nTesting auth backend:")
    auth_admin = authenticate(username='admin@example.com', password='adminpass')
    auth_user = authenticate(username='user@example.com', password='userpass')
    
    print(f"   Admin auth result: {'✓' if auth_admin else '✗'}")
    print(f"   User auth result: {'✓' if auth_user else '✗'}")
    
    if not (auth_admin and auth_user):
        return False
    
    # Test 4: Test web login
    print("\nTesting web login:")
    client = Client()
    
    # Test admin login
    response = client.post('/login/', {
        'email': 'admin@example.com',
        'password': 'adminpass'
    })
    admin_login_success = response.status_code == 302  # Redirect means success
    print(f"   Admin web login: {'✓' if admin_login_success else '✗'}")
    
    # Test user login
    client = Client()  # Fresh client
    response = client.post('/login/', {
        'email': 'user@example.com', 
        'password': 'userpass'
    })
    user_login_success = response.status_code == 302  # Redirect means success
    print(f"   User web login: {'✓' if user_login_success else '✗'}")
    
    if not (admin_login_success and user_login_success):
        print(f"   Admin response status: {response.status_code}")
        print(f"   Response content: {response.content.decode()[:200]}...")
        return False
    
    print("\nAll tests passed! ✓")
    print("\nTest accounts:")
    print("  Admin: admin@example.com / adminpass")
    print("  User:  user@example.com / userpass")
    print("\nRun: ./run_server.sh then visit http://127.0.0.1:8000/login/")
    
    return True

if __name__ == "__main__":
    try:
        test_authentication()
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()