from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = None
    phone_number = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    invite_code_activated = models.BooleanField(default=False)
    outher_invite_code = models.CharField(max_length=6, null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def full_name(self):
        return self.name + ' ' + self.phone_number

    def __str__(self):
        return self.phone_number