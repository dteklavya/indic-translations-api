"""tests.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 16:54:33"
__credits__ = ["Rajesh Pethe"]


from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest import TestCase, mock
import os
import base64
from io import BytesIO

User = get_user_model()


class TestTranslationAPI(TestCase):
    def setUp(self) -> None:
        os.environ["userID"] = "test"
        os.environ["ulcaApiKey"] = "mock_key"
        os.environ["DefaultPipeLineId"] = "mock_id"
        self.user = User.objects.create_user(
            username="testuser", email="test@trans.com", password="password"
        )
        self.client = APIClient()
        return super().setUp()

    def tearDown(self) -> None:
        self.user.delete()
        return super().tearDown()

    def test_auth_required_for_translate(self):
        response = self.client.post(
            "/api/translate/",
            {"sourceLanguage": "en", "targetLanguage": "hi", "text": "hello"},
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_translate_end_point(self):
        response = self.client.post(
            "/api/token/", data={"username": "testuser", "password": "password"}
        )
        token = response.data.get("access")

        with mock.patch(
            "bhashini_translator.bhashini_translator.Bhashini.translate"
        ) as mock_main:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

            mock_main.return_value = "mock translated text"

            response = self.client.post(
                "/api/translate/",
                {"sourceLanguage": "en", "targetLanguage": "hi", "text": "hello"},
            )
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, "mock translated text")

    def test_auth_required_tts(self):
        response = self.client.post(
            "/api/tts/",
            {"sourceLanguage": "en", "text": "hello"},
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tts_end_point(self):
        response = self.client.post(
            "/api/token/", data={"username": "testuser", "password": "password"}
        )
        token = response.data.get("access")

        with mock.patch(
            "bhashini_translator.bhashini_translator.Bhashini.tts"
        ) as mock_main:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

            mockstr = b"mock base64 encode string"
            return_value = BytesIO()
            buffer = BytesIO()
            buffer.write(mockstr)
            base64.encode(buffer, return_value)

            mock_main.return_value = return_value.getvalue()

            response = self.client.post(
                "/api/tts/",
                {"sourceLanguage": "en", "text": "hello"},
            )
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.as_attachment)
