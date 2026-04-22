from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):
    """
    Switch MentorshipSession.id and Review.id to ObjectIdField.
    No database operation needed — MongoDB is schemaless.
    """

    dependencies = [
        ('mentorship_sessions', '0002_mentorshipsession_scheduled_at'),
        ('users', '0003_objectid_pk'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='mentorshipsession',
                    name='id',
                    field=djongo.models.fields.ObjectIdField(),
                ),
                migrations.AlterField(
                    model_name='review',
                    name='id',
                    field=djongo.models.fields.ObjectIdField(),
                ),
            ],
        ),
    ]
