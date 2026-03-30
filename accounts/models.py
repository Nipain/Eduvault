from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('accountant','Accountant'),
        ('teacher','Teacher'),
        ('parent','Parent'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    school = models.ForeignKey('tenants.School', on_delete=models.CASCADE, null=True, blank=True)