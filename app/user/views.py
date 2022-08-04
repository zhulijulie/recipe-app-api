"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # uses the default renderer class for this obtain our token view.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    # what that auth user can access
    permission_classes = [permissions.IsAuthenticated]

    # when you make a http get request to this endpoint, it's going to
    # call getobjects to get the user, it's going to retrieve the user
    # that was authenticated and then it's going to run it through our
    # serializer that we defined before returning the result to the API.
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
