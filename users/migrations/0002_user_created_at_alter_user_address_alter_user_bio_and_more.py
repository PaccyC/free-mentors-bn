from django.db import migrations


class Migration(migrations.Migration):
    """No-op: MongoDB is schemaless, no ALTER needed."""

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = []
