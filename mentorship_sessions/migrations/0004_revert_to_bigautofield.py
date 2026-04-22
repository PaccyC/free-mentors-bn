import django.db.models
from django.db import migrations


class Migration(migrations.Migration):
    """Revert id fields back to BigAutoField."""

    dependencies = [
        ('mentorship_sessions', '0003_objectid_pk'),
        ('users', '0004_revert_to_bigautofield'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='mentorshipsession',
                    name='id',
                    field=django.db.models.BigAutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID',
                    ),
                ),
                migrations.AlterField(
                    model_name='review',
                    name='id',
                    field=django.db.models.BigAutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID',
                    ),
                ),
            ],
        ),
    ]
