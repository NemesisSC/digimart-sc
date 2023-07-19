from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Account(models.Model):
    choices = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=10, choices=choices, default='male')
    city = models.CharField(max_length=500, null = True, blank=True)
    address = models.CharField(max_length=500, null = True, blank=True)
    phone_no = models.CharField(max_length=15)
