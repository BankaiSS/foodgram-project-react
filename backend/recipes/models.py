from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    """ Модель Ингридиент """

    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', null=True)
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX!'
            )
        ]
    )
    slug = models.SlugField(max_length=200, null=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['pk']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов"""
    author = models.ForeignKey(to=User, related_name='recipes',
                               on_delete=models.CASCADE,
                               verbose_name='Author')
    name = models.CharField(verbose_name='Name', max_length=50, blank=False)
    image = models.ImageField(upload_to='recipes/images/',
                              blank=False, verbose_name='Image')
    text = models.TextField(verbose_name='Description', blank=False,
                            max_length=2000)
    ingredients = models.ManyToManyField(to=Ingredient,
                                         verbose_name='Ingredients',
                                         blank=False,
                                         related_name='recipes',
                                         through='IngredientsInRecipe',)
    tags = models.ManyToManyField(to=Tag, blank=False, verbose_name='tags',
                                  )
    cooking_time = models.PositiveIntegerField(blank=False,
                                               verbose_name='Cooking time')
    pub_date = models.DateTimeField(verbose_name='Date of publication',
                                    auto_now_add=True, blank=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    """ Модель для связи Ингридиента и Рецепта """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1, message='Минимальное количество 1!')]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit}) - {self.amount} '
        )


class Favourite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites',
                             verbose_name='User',
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favourites',
                               verbose_name='Recipe',
                               )

    class Meta:
        verbose_name = 'Favourite'
        verbose_name_plural = 'Favourites'
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user_id} {self.recipe_id}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_list_user',
                             verbose_name='User',
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_list_recipe',
                               verbose_name='Recipe',
                               )

    class Meta:
        verbose_name = 'Shop-list'
        verbose_name_plural = 'Shop-lists'
        constraints = (
            UniqueConstraint(fields=('user', 'recipe'),
                             name='unique_shopping_list'),
        )

    def __str__(self):
        return f'{self.user_id} {self.recipe_id}'
