"""tests.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 16:54:33"
__credits__ = ["Rajesh Pethe"]


from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest import TestCase, mock, main
import os

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

    def test_auth_required(self):
        response = self.client.post(
            "/api/translate/",
            {"sourceLanguage": "en", "targetLanguage": "hi", "text": "hello"},
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_translate_end_point(self):
        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "translation",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "sourceScriptCode": "Latn",
                                "targetLanguage": "hi",
                                "targetScriptCode": "Deva",
                            },
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        response = self.client.post(
            "/api/token/", data={"username": "testuser", "password": "password"}
        )
        token = response.data.get("access")

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.Bhashini.compute_response"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200

            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200

            response = self.client.post(
                "/api/translate/",
                {"sourceLanguage": "en", "targetLanguage": "hi", "text": "hello"},
            )
            self.assertIsNotNone(response)
