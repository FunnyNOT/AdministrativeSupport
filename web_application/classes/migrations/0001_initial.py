# Generated by Django 4.1.2 on 2022-10-28 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0002_initiate_portal_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('assigned_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_teacher', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('portal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portals.portal')),
            ],
            options={
                'verbose_name_plural': 'Classes',
                'db_table': 'classes',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('belongs_to_class', models.BooleanField()),
                ('absences', models.IntegerField()),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
            ],
            options={
                'verbose_name_plural': 'Students',
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='StudentGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grades', models.TextField()),
                ('average_grade', models.DecimalField(decimal_places=3, max_digits=5)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.student')),
            ],
            options={
                'verbose_name_plural': 'StudentsGrades',
                'db_table': 'students_grades',
            },
        ),
    ]
