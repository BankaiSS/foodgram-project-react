from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    """Модель для ингредиентов рецепта"""
    name = models.CharField(max_length=200, verbose_name='Name')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='measurement_unit',)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['pk']

    def __str__(self):
        return self.name


class Tags(models.Model):
    """Модель для тегов рецептов"""
    name = models.CharField(max_length=200, verbose_name='Name', null=True)
    color = models.CharField(max_length=7, null=True, verbose_name='Color')
    slug = models.SlugField(max_length=200, null=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['pk']

    def __str__(self):
        return self.name


class Recipes(models.Model):
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
    tags = models.ManyToManyField(to=Tags, blank=False, verbose_name='tags',
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
    """Модель для добавления ингредиентов в рецепт"""
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    amount = models.PositiveIntegerField(verbose_name='Amount',)

    class Meta:
        verbose_name = 'Ingredient in recipe'
        verbose_name_plural = 'Ingredients in recipe'
        constraints = (
            UniqueConstraint(fields=('recipe', 'ingredient'),
                             name='recipeingredient'),
        )

    def __str__(self):
        return f'{self.recipe_id} {self.ingredient_id}'


class Favourites(models.Model):
    """Модель для списка избранного"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites',
                             verbose_name='User',
                             )
    recipe = models.ForeignKey(Recipes,
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
    """Модель для списка покупок"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_list_user',
                             verbose_name='User',
                             )
    recipe = models.ForeignKey(Recipes,
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
