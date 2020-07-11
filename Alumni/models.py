from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phone_field import PhoneField

from Home.models import Skill, Job, Major


class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='alumni_user')
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    phone_number = PhoneField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    skills = models.ManyToManyField(Skill, related_name='alumni_skills')
    majors = models.ManyToManyField(Major, related_name='alumni_majors')
    jobs_applied = models.ManyToManyField(Job, through='AlumniJobApplication')
    dp = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    cv = models.FileField(upload_to='documents', default='../staticfiles/DefaultCV.txt')

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name


class AlumniJobApplication(models.Model):
    job_id = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='alumni_job')
    applied = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='alumni_apply')
    date_applied = models.DateTimeField(null=True, auto_now_add=True)
