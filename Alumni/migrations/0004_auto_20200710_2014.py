# Generated by Django 2.2.13 on 2020-07-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumni', '0003_auto_20200710_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='alumni',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
