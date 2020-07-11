# Generated by Django 2.2.13 on 2020-07-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_major'),
        ('Alumni', '0004_auto_20200710_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='majors',
            field=models.ManyToManyField(related_name='alumni_majors', to='Home.Major'),
        ),
    ]