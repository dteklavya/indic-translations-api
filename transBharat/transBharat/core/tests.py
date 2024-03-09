"""tests.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/08/2024 12:01:14"
__credits__ = ["Rajesh Pethe"]


from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@trans.com", password="password"
        )
        self.client = APIClient()

    def test_login(self):
        response = self.client.post(
            "/api/token/", data={"username": "testuser", "password": "password"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_logout(self):
        self.client.force_login(self.user)
        token = RefreshToken.for_user(self.user)
        response = self.client.post("/api/logout/", {"refresh": str(token)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure token has been invalidated/blacklisted
        response = self.client.post("/api/token/refresh/", {"refresh": str(token)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        self.client.force_login(self.user)
        token = RefreshToken.for_user(self.user)
        response = self.client.post("/api/token/refresh/", {"refresh": str(token)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
