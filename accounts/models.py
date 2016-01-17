from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
  savings = models.IntegerField(default=0)
  scheduled_deposit = models.IntegerField(default=0)
  scheduled_frequency = models.CharField(max_length=30,
    choices=[('day', 'day'),('week', 'week'),('month', 'month')], null=True)
  scheduled_days_left = models.IntegerField(default=1) #day=1,week=7,month=30 -- for deposit cycle
  active = models.BooleanField(default=False)
  token = models.CharField(max_length=100, null=True)
  bank_amount = models.IntegerField(default=0)
  bank_name = models.CharField(max_length=100, null=True)

class Goal(models.Model):
  name = models.CharField(max_length=100)
  amount = models.IntegerField()
  owner = models.ForeignKey(Account,)

class History(models.Model):
	date = models.DateField(auto_now=False, auto_now_add=False)
	balance = models.IntegerField(default=0)
	owner = models.ForeignKey(Account,)