# Generated by Django 2.2.13 on 2020-07-19 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_auto_20200715_1228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'get_latest_by': 'date_posted'},
        ),
    ]