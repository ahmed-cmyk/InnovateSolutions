# Generated by Django 2.2.13 on 2020-08-11 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumni', '0009_auto_20200716_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='is_active',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=10),
        ),
    ]
