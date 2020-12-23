import os

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import threading

# Create your models here.
from Admin.models import Admin

from DjangoUnlimited.settings import EMAIL_HOST_USER
from Employer.models import Employer


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)

        while self.exists(name) or (max_length and len(name) > max_length):
            date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            name = os.path.join(dir_name, "%s_%s%s" % (file_root, date, file_ext))
            if max_length is None:
                continue
            truncation = len(name) - max_length
            if truncation > 0:
                file_root = file_root[:-truncation]
                if not file_root:
                    raise SuspiciousFileOperation(
                        'Storage can not find an available filename for "%s". '
                        'Please make sure that the corresponding file field '
                        'allows sufficient "max_length".' % name
                    )
                name = os.path.join(dir_name, "%s_%s%s" % (file_root, date, file_ext))
        return name

class Industry(models.Model):
    industry_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.industry_name = self.industry_name.capitalize()

    def __str__(self):
        name = self.industry_name
        return name

    class Meta:
        verbose_name_plural = 'Industries'


class Skill(models.Model):
    skill_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.skill_name = self.skill_name.capitalize()

    def __str__(self):
        name = self.skill_name
        return name


class Major(models.Model):
    major_name = models.CharField(max_length=50, unique=True)

    def clean(self):
        self.major_name = self.major_name.capitalize()

    def __str__(self):
        name = self.major_name
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
        ('Ra’s al-Khaimah', 'Ra’s al-Khaimah'),
        ('Remote', 'Remote'),
    ]
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    ]
    JOB_STATUS = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Deleted', 'Deleted')
    ]
    JOB_LEVEL = [
        ('Unspecified', 'Unspecified'),
        ('Entry', 'Entry'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior')
    ]
    DURATION = [
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Permanent', 'Permanent'),
    ]
    date_posted = models.DateField(null=False, blank=False, auto_now_add=True)
    posted_by = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_author', blank=True)
    job_title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    description_upload = models.FileField(upload_to='documents', storage=OverwriteStorage(), null=True, blank=True)
    status = models.CharField(max_length=15, choices=JOB_STATUS, default='Open')
    date_closed = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    job_type_id = models.ForeignKey(JobType, on_delete=models.CASCADE, related_name='job_type')
    industry_id = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='job_industry')
    job_level = models.CharField(max_length=15, choices=JOB_LEVEL, null=True, blank=True, default='Unspecified')
    duration_type = models.CharField(max_length=10, choices=DURATION)
    duration = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    salary_min = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    salary_max = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    skills = models.ManyToManyField(Skill, related_name='job_skills')
    is_active = models.CharField(blank=True, max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[2][1])
    other_skills = models.TextField(null=True, blank=True)

    def __str__(self):
        title = self.job_title
        return title

    def __iter__(self):
        return [
            self.job_title,
            self.location,
            self.duration,
            self.duration_type,
            self.salary_min,
            self.salary_max,
            self.skills
        ]

    class Meta:
        get_latest_by = 'date_posted'


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


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()
