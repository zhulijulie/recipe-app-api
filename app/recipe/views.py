"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,  # can mix in a view to add functions
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


# ModelViewSet is specifically set up to work directly with a model
# because we're going to use a lot of the existing logic that's
# provided by the serializer in order to perform a create read, update
# and delete operations.
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    # ViewSet will generate multiple endpoints automatically
    # such as list and detail(id) view
    serializer_class = serializers.RecipeDetailSerializer
    # queryset rep. the objects that available for this viewset
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # overwrite get_queryset by only show recipes for that user
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    # already validated serializer as param
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


# use ViewSet since it gonna be basic CRUD
# GenericViewSet MUST be the last one in the import
class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # by default it returns all tags, overridden to return only for that user
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
