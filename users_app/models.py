from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Job(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    job = models.ForeignKey("Job", on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.user.username
