# Generated by Django 2.2.15 on 2020-08-25 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='posted_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_author', to='Employer.Employer'),
        ),
    ]
