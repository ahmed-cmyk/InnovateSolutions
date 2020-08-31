from django.core.exceptions import SuspiciousFileOperation
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

from Home.models import Skill, Job, Major

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

class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='alumni_user')
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    ]
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    student_id = models.CharField(max_length=8, null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name='alumni_skills')
    majors = models.ManyToManyField(Major, related_name='alumni_majors')
    jobs_applied = models.ManyToManyField(Job, through='AlumniJobApplication')
    dp = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    cv = models.FileField(upload_to='documents', storage=OverwriteStorage(), default='../staticfiles/DefaultCV.txt')
    is_active = models.CharField(blank=True, max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[2][1])

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name


class AlumniJobApplication(models.Model):
    job_id = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='alumni_job')
    applied = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='alumni_apply')
    date_applied = models.DateTimeField(null=True, auto_now_add=True)

