# Generated by Django 4.0.4 on 2022-06-10 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('users', models.IntegerField(default=0)),
                ('is_active', models.BooleanField()),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Portals',
                'db_table': 'portals',
            },
        ),
        migrations.AddIndex(
            model_name='portal',
            index=models.Index(fields=['name', 'is_active'], name='portals_name_fa4f5f_idx'),
        ),
    ]