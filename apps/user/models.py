from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    avatar = models.ImageField(
        null=True,
        blank=True
    )
