from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    phone_number = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=255)  # Добавьте максимальную длину для имени
    otp = models.CharField(max_length=4, null=True, blank=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def full_name(self):  # Измените имя метода, чтобы избежать конфликта с полем "name"
        return self.name + ' ' + self.phone_number

    def __str__(self):
        return self.phone_number