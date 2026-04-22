from django.db import migrations


class Migration(migrations.Migration):
    """No-op: MongoDB is schemaless, field available without ALTER TABLE."""

    dependencies = [
        ('mentorship_sessions', '0001_initial'),
    ]

    operations = []
