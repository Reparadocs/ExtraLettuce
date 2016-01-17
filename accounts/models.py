from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
  savings = models.IntegerField(default=0)
  scheduled_deposit = models.IntegerField(default=0)
  scheduled_frequency = models.CharField(max_length=30,
    choices=[('day', 'day'),('week', 'week'),('month', 'month')], null=True)
  active = models.BooleanField(default=False)
  token = models.CharField(max_length=100, null=True)
