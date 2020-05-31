from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

# Model for Post in Bulletin
class Post(models.Model):
    title = models.CharField(max_length=100)
    feed = models.TextField()
    release_date = models.DateTimeField(default=datetime.now, null=True)
    update_date = models.DateTimeField(default=datetime.now, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_name')
    author_updated = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_updated')
    status = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'release_date'
