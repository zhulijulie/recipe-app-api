"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'

# Django expects a natural function for this parameter here, we use the as_view method to
# get that view function. That is the way that Django rest framework converts the corres
# base view into the supported Django view.
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
