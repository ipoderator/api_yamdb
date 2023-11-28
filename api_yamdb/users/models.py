from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ANONIMOUS = 'anonimous'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
        (ANONIMOUS, 'anonimous')
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")])
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Электронная почта',
        unique=True
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        default=USER,
        choices=ROLES,
        max_length=30,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Код подтверждения'
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    def __str__(self):
        return self.username
