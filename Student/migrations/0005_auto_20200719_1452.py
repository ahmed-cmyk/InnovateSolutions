# Generated by Django 2.2.13 on 2020-07-19 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0004_student_majors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='DOB',
            new_name='date_of_birth',
        ),
    ]
