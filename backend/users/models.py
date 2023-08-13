from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False,
                              verbose_name='Email')
    username = models.CharField(verbose_name='Username',
                                unique=True,
                                max_length=150)
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='Name')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='Last name')
    password = models.CharField(max_length=150, verbose_name='Password',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name', ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(fields=('email', 'username'),
                                    name='unique_auth'),
        )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(to=User, verbose_name='Subscriber',
                                   on_delete=models.CASCADE,
                                   related_name='subscriber')
    author = models.ForeignKey(to=User, verbose_name='Author',
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('subscriber', 'author'),
                             name='unique_subscription'),
        )

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
