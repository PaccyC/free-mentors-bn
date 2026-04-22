from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorshipSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.TextField()),
                ('status', models.CharField(
                    choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined')],
                    default='PENDING',
                    max_length=10,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('mentee', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sessions_as_mentee',
                    to='users.user',
                )),
                ('mentor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sessions_as_mentor',
                    to='users.user',
                )),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField()),
                ('is_hidden', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('mentee', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reviews_given',
                    to='users.user',
                )),
                ('mentor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reviews_received',
                    to='users.user',
                )),
            ],
        ),
    ]
