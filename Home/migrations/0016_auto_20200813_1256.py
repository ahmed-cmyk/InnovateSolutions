# Generated by Django 2.2.13 on 2020-08-13 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0015_auto_20200813_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_author', to='Employer.Employer'),
        ),
    ]
