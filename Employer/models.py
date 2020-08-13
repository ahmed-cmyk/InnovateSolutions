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
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    ]
    company_name = models.CharField(max_length=50)
    company_description = models.TextField()
    phone_number = PhoneField(blank=False)
    logo = models.ImageField(upload_to='company_logos', null=True, blank=True)
    contact_name = models.CharField(max_length=50, blank=False, default='N/A')
    trade_license = models.FileField(upload_to='trade_licenses', null=False, blank=False,
                                     default='../staticfiles/DefaultDP.jpg')

    is_active = models.CharField(blank=True, max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[2][1])

    def __str__(self):
        name = self.user.__str__()
        return name
