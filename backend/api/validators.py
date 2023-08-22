from rest_framework import exceptions

from users.models import User

NOT_TO_USE_USERNAMES = ('me', 'set_password', 'subscribe', 'subscriptions')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise exceptions.ValidationError('Email уже занят.'
                                         'Пожалуйста, используйте другую!')
    return value


def validate_username(value):
    value = value.lower()
    if value in NOT_TO_USE_USERNAMES:
        raise exceptions.ValidationError('Некорректный username.n\
                                          Пожалуйста, исправьте!')
    return value
