from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):
    """
    Switch User.id from AutoField to ObjectIdField so Django's id maps to
    MongoDB's _id. No database operation needed — MongoDB is schemaless.
    """

    dependencies = [
        ('users', '0002_user_created_at_alter_user_address_alter_user_bio_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='user',
                    name='id',
                    field=djongo.models.fields.ObjectIdField(),
                ),
            ],
        ),
    ]
