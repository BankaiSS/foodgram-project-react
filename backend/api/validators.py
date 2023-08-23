from django.shortcuts import get_object_or_404
from recipes.models import Ingredient
from rest_framework import exceptions, status
from rest_framework.exceptions import ValidationError
from users.models import Subscription, User

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


def validate_ingredients(self, value):
    ingredients = value
    if not ingredients:
        raise ValidationError({
            'ingredients': 'Нужен хотя бы один ингредиент!'
        })
    ingredients_list = []
    for item in ingredients:
        ingredient = get_object_or_404(Ingredient, id=item['id'])
        if ingredient in ingredients_list:
            raise ValidationError({
                'ingredients': 'Ингридиенты не могут повторяться!'
            })
        if int(item['amount']) <= 0:
            raise ValidationError({
                'amount': 'Количество ингредиента должно быть больше 0!'
            })
        ingredients_list.append(ingredient)
    return value


def validate_tags(self, value):
    tags = value
    if not tags:
        raise ValidationError({'tags': 'Нужно выбрать хотя бы один тег!'})
    tags_list = []
    for tag in tags:
        if tag in tags_list:
            raise ValidationError({'tags':
                                  'Теги должны быть уникальными!'})
        tags_list.append(tag)
    return value


def validate_subscription(self, data):
    author = self.instance
    user = self.context.get('request').user
    if Subscription.objects.filter(author=author, user=user).exists():
        raise ValidationError(
            detail='Вы уже подписаны на этого пользователя!',
            code=status.HTTP_400_BAD_REQUEST
        )
    if user == author:
        raise ValidationError(
            detail='Вы не можете подписаться на самого себя!',
            code=status.HTTP_400_BAD_REQUEST
        )
    return data
