# Generated by Django 4.0.5 on 2022-09-20 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100)),
                ('body', models.TextField()),
                ('is_active', models.BooleanField()),
                ('visible_to_students', models.BooleanField(blank=False, null=False)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('portal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portals.portal')),
            ],
            options={
                'verbose_name_plural': 'Announcements',
                'db_table': 'announcements',
            },
        ),
    ]
