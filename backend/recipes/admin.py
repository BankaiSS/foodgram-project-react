from django.contrib import admin

from .models import Favourites, IngredientsInRecipe, Recipes, ShoppingList


class RecipesInline(admin.StackedInline):
    model = IngredientsInRecipe
    min_num = 1


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'recipe_in_favorites',
    )
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipesInline,)

    def recipe_in_favorites(self, instance):
        return instance.favourites.count()


@admin.register(IngredientsInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Favourites)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingList)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
