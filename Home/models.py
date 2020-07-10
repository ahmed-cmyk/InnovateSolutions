from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
from Admin.models import Admin
from django.db.models import ManyToManyField


class Industry(models.Model):
    industry_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.industry_name = self.industry_name.capitalize()

    def __str__(self):
        name = self.industry_name
        return name


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.skill_name = self.skill_name.capitalize()

    def __str__(self):
        name = self.skill_name
        return name


class JobType(models.Model):
    type_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.type_name = self.type_name.capitalize()

    def __str__(self):
        name = self.type_name
        return name


class Job(models.Model):
    LOCATION_CHOICES = [
        ('Abu Dhabi', 'Abu Dhabi'),
        ('Dubai', 'Dubai'),
        ('Sharjah', 'Sharjah'),
        ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
        ('Fujairah', 'Fujairah'),
        ('Ajman', 'Ajman'),
        ('Ra’s al-Khaimah', 'Ra’s al-Khaimah')
    ]
    date_posted = models.DateField(null=False, blank=False, auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_author')
    job_title = models.CharField(max_length=100)
    description = models.TextField()
    job_status = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Deleted', 'Deleted')
    ]
    status = models.CharField(max_length=15, choices=job_status, default='Open')
    date_closed = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    job_type_id = models.ForeignKey(JobType, on_delete=models.CASCADE, related_name='job_type')
    industry_id = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='job_industry')
    duration = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    salary = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    skills = models.ManyToManyField(Skill, related_name='job_skills')

    def __str__(self):
        title = self.job_title
        return title


class HelpDeskComplaints(models.Model):
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complainant')
    subject = models.CharField(max_length=100)
    details = models.TextField()
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='assigned_admin')


# User notifications.
class UserNotifications(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    notification = models.TextField()
    type = models.CharField(max_length=100)
    to_show = models.BooleanField(default=True)
    date_time = models.DateTimeField(default=datetime.now)
