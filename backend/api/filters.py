from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import Recipes
from users.models import User


class NameSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(rest_framework.FilterSet):
    author = rest_framework.ModelChoiceFilter(queryset=User.objects.all())
    tags = rest_framework.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = rest_framework.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipes
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favourites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                shopping_list_recipe__user=self.request.user)
        return queryset
