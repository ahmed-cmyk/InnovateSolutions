# Generated by Django 2.2.13 on 2020-08-12 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0013_job_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='other_skills',
            field=models.TextField(blank=True, null=True),
        ),
    ]
