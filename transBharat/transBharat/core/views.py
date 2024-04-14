"""views.py: Core views - primarily authentication related"""

__author__ = "Rajesh Pethe"
__date__ = "04/13/2024 18:12:53"
__credits__ = ["Rajesh Pethe"]


from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class LogoutView(APIView):
    """
    Logs out user by black-listing JW token if any.
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
