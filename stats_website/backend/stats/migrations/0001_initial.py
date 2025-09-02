# Generated manually to avoid migration conflicts
# This migration marks tables as managed without creating them
# The actual tables are created by the vacation_website app

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        # No operations - tables already exist from vacation_website
        # This migration just marks the app as migrated
    ]