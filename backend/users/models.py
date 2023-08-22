from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
    )
    username = models.CharField(verbose_name='Username',
                                unique=True,
                                max_length=150)
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='Name')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='Last name')
    password = models.CharField(max_length=150, verbose_name='Password',)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(fields=('email', 'username'),
                                    name='unique_auth'),
        )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(fields=['subscriber', 'author'], name='unique_subscription')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'