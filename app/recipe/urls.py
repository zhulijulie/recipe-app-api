"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# create a new endpoint api/recipes and it will assign all of the
# different endpoints from our recipe viewset to that endpoint.
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

# use the include function to include the URLs that are generated
# automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]