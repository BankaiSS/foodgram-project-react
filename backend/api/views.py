from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import NameSearchFilter, RecipeFilter
from api.pagination import CustomPagination
from recipes.models import (Favourite, Ingredient, IngredientsInRecipe,
                            Recipe, ShoppingList, Tag)
from users.models import Subscription, User
from . import serializers
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (IngredientsSerializer, RecipeForShopAndFavSerializer,
                          RecipesPostUpdateDeleteSerializer, RecipesSerializer,
                          SetPasswordSerializer, SubscribeAuthorSerializer,
                          SubscriptionsSerializer, TagsSerializer)


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    pagination_class = CustomPagination

    user_seriliazer = {
        'list': serializers.UserSerializer,
        'retrieve': serializers.UserSerializer,
        'me': serializers.UserSerializer,
        'create': serializers.UserPostSerializer,
        'subscribe': serializers.SubscribeAuthorSerializer,
        'subscriptions': serializers.SubscriptionsSerializer,
        'set_password': serializers.SetPasswordSerializer}

    def get_user(self):
        return self.request.user

    def get_serializer_class(self):
        return self.user_seriliazer.get(self.action)

    @action(detail=False,
            permission_classes=[IsAuthenticated],)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_user
        return self.retrieve(request, *args, **kwargs)

    @action(["POST"],
            detail=False,
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.validated_data
                                       ['new_password'])
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated],)
    def subscriptions(self, request):
        queryset = User.objects.filter(following__subscriber=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(page, many=True,
                                             context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(["POST", "DELETE"], detail=True,
            permission_classes=[IsAuthorOrAdminOrReadOnly])
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = SubscribeAuthorSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save(subscriber=request.user, author=author)
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)

        get_object_or_404(Subscription, subscriber=request.user,
                          author=author).delete()
        return Response({'detail': 'Отписка'},
                        status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (NameSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags',
                                               'recipe_ingredients').all()
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = CustomPagination
    serializer_class = RecipesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesSerializer

        elif self.request.method == 'POST' or 'PATCH':
            return RecipesPostUpdateDeleteSerializer

    def handle_post_request(self, request, model, error_message, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        serializer = RecipeForShopAndFavSerializer(
            recipe, data=request.data,
            context={"request": request})
        serializer.is_valid(raise_exception=True)
        if not model.objects.filter(user=request.user, recipe=recipe).exists():
            model.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': error_message},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):
        FILENAME = 'your_shopping_cart.txt'
        ingredients = (
            IngredientsInRecipe.objects.filter(
                recipe__shopping_list_recipe__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(number=Sum('number'))
        )
        result = '\n'.join(
            (
                f'{ingredient["ingredient__name"]} - {ingredient["number"]}/'
                f'{ingredient["ingredient__measurement_unit"]}'
                for ingredient in ingredients
            )
        )
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={FILENAME}'
        return response

    @action(["POST", "DELETE"], detail=True,
            permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, **kwargs):
        if request.method == 'POST':
            return self.handle_post_request(request, ShoppingList,
                                            'Рецепт уже в списке покупок.',
                                            **kwargs)

    @action(["POST", "DELETE"], detail=True,
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, **kwargs):
        if request.method == 'POST':
            return self.handle_post_request(request, Favourite,
                                            'Рецепт уже в избранном.',
                                            **kwargs)
