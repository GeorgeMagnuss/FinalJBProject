# Empty initial migration for stats app with unmanaged models
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        # No operations needed - all models are unmanaged (managed = False)
    ]