# Generated by Django 2.2.15 on 2020-08-25 07:16

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0001_initial'),
        ('Employer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.TextField()),
                ('type', models.CharField(max_length=100)),
                ('to_show', models.BooleanField(default=True)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateField(auto_now_add=True)),
                ('job_title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Deleted', 'Deleted')], default='Open', max_length=15)),
                ('date_closed', models.DateField(blank=True, null=True)),
                ('location', models.CharField(choices=[('Abu Dhabi', 'Abu Dhabi'), ('Dubai', 'Dubai'), ('Sharjah', 'Sharjah'), ('Umm al-Qaiwain', 'Umm al-Qaiwain'), ('Fujairah', 'Fujairah'), ('Ajman', 'Ajman'), ('Ra’s al-Khaimah', 'Ra’s al-Khaimah')], max_length=100)),
                ('duration', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('duration_type', models.CharField(choices=[('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Permanent', 'Permanent')], max_length=10)),
                ('salary_min', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('salary_max', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('is_active', models.CharField(blank=True, choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('other_skills', models.TextField(blank=True, null=True)),
                ('industry_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_industry', to='Home.Industry')),
                ('job_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_type', to='Home.JobType')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_author', to='Employer.Employer')),
                ('skills', models.ManyToManyField(related_name='job_skills', to='Home.Skill')),
            ],
            options={
                'get_latest_by': 'date_posted',
            },
        ),
        migrations.CreateModel(
            name='HelpDeskComplaints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_admin', to='Admin.Admin')),
                ('user_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complainant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
