# Generated by Django 2.2.6 on 2020-06-21 10:05

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='phone_number',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
    ]