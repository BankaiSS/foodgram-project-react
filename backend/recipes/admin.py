from django.contrib import admin

from .models import Favourite, IngredientsInRecipe, Recipe, ShoppingList


class RecipesInline(admin.StackedInline):
    model = IngredientsInRecipe
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'recipe_in_favorites',
    )
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipesInline,)

    def recipe_in_favorites(self, instance):
        return instance.favourite.count()


@admin.register(IngredientsInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Favourite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingList)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
