from datetime import datetime

from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class HelpDeskModel(models.Model):
    name_Request = models.ForeignKey(User, on_delete=models.CASCADE, related_name='name_ITRequest')
    subject = models.CharField(max_length=255, null=False)
    issue = models.TextField()
    issue_date = models.DateTimeField(default=datetime.now, null=False)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(default=None, null=True)