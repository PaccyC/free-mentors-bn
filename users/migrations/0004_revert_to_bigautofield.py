import django.db.models
from django.db import migrations


class Migration(migrations.Migration):
    """Revert id back to BigAutoField — ObjectIdField incompatible with existing integer-id data."""

    dependencies = [
        ('users', '0003_objectid_pk'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='user',
                    name='id',
                    field=django.db.models.BigAutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID',
                    ),
                ),
            ],
        ),
    ]
