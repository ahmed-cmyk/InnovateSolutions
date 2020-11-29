from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.validators import RegexValidator

from django.db.models.signals import post_save
from django.dispatch import receiver


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employer_user')
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    ]
    company_name = models.CharField(max_length=50)
    company_description = models.TextField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999' or all numbers. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    logo = models.ImageField(upload_to='company_logos', null=True, blank=True)
    contact_name = models.CharField(max_length=50, blank=False, default='N/A')
    trade_license = models.FileField(upload_to='trade_licenses', null=True, blank=True)
    company_website = models.URLField(blank=True)
    is_active = models.CharField(blank=True, max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[2][1])

    def __str__(self):
        name = self.user.__str__()
        return name
