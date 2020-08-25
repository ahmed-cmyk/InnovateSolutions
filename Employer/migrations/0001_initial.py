# Generated by Django 2.2.15 on 2020-08-25 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employer_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=50)),
                ('company_description', models.TextField()),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos')),
                ('contact_name', models.CharField(default='N/A', max_length=50)),
                ('trade_license', models.FileField(default='../media/trade_licenses/ICT108_Assignment.pdf', upload_to='trade_licenses')),
                ('company_website', models.URLField(blank=True)),
                ('is_active', models.CharField(blank=True, choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=10)),
            ],
        ),
    ]
