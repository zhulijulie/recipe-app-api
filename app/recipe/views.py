"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
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
