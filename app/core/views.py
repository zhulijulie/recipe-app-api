"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])  # use decorator to let api return simple response
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
