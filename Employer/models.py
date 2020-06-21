from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from phone_field import PhoneField

from django.db.models.signals import post_save
from django.dispatch import receiver
from Home.models import Industry

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employer_user')
    company_name = models.CharField(max_length=50)
    company_description = models.TextField()
    phone_number = PhoneField(blank=True)
    logo = models.ImageField(upload_to='company_logos', null=True, blank=True)

    def __str__(self):
        name = self.company_name
        return name