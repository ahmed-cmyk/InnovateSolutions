# Generated by Django 2.2.15 on 2020-08-18 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employer', '0011_auto_20200817_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='trade_license',
            field=models.FileField(default='../media/trade_licenses/ICT108_Assignment.pdf', upload_to='trade_licenses'),
        ),
    ]
