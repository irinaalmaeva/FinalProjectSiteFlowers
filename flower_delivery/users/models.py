from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)  # Телефон пользователя
    address = models.TextField(blank=True)  # Адрес для доставки

    def __str__(self):
        return self.username
