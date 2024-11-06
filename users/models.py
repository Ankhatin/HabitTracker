from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    tg_id = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="ID пользователя в телеграм",
        **NULLABLE
    )
    tg_username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="username пользователя в телеграм",
        help_text="Укажите свой username в Telegram",
    )
    phone = models.CharField(
        max_length=20, unique=True, verbose_name="Телефон", **NULLABLE
    )
    city = models.CharField(max_length=30, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="media/users/", verbose_name="Аватар", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["tg_username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
