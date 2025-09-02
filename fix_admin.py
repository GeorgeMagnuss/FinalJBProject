#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VacationProjectGM.settings')
django.setup()

from vacations.models import User

try:
    admin = User.objects.get(email='admin@vacation.com')
    admin.set_password('admin123')
    admin.save()
    print('✅ Admin password fixed successfully')
    print(f'Password check: {admin.check_password("admin123")}')
except Exception as e:
    print(f'❌ Error: {e}')