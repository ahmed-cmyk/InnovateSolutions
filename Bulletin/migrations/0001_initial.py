# Generated by Django 2.2.15 on 2020-08-25 07:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('feed', models.TextField()),
                ('release_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('update_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_name', to=settings.AUTH_USER_MODEL)),
                ('author_updated', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'release_date',
            },
        ),
    ]
