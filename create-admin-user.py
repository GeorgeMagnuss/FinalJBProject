#!/usr/bin/env python3
"""
Create admin user for both vacation and stats systems
Run this inside the vacation_website container
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacation_project.settings')
django.setup()

from vacations.models import User, Role
from django.contrib.auth.hashers import make_password

def create_admin_user():
    try:
        # Get or create admin role
        admin_role, created = Role.objects.get_or_create(role_name='admin')
        
        # Create or update admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': admin_role,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'password': make_password('adminpass')
            }
        )
        
        if not created:
            # Update existing user
            admin_user.set_password('adminpass')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.is_active = True
            admin_user.role = admin_role
            admin_user.save()
            print("✅ Updated existing admin user")
        else:
            print("✅ Created new admin user")
            
        print(f"Admin user: {admin_user.email}")
        print(f"Password: adminpass")
        print(f"Is admin: {admin_user.is_admin}")
        print(f"Is staff: {admin_user.is_staff}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        
if __name__ == "__main__":
    create_admin_user()