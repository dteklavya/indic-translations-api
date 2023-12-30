import requests, os
from dotenv import load_dotenv
import json


load_dotenv()


class BhashiniTranslator:
    ulcaUserId: str
    ulcaApiKey: str
    sourceLanguage: str
    targetLanguage: str
    pipeLineData: dict

    def __init__(self) -> None:
        self.ulcaUserId = os.environ.get("userID")
        self.ulcaApiKey = os.environ.get("ulcaApiKey")
        if not self.ulcaUserId or not self.ulcaApiKey:
            raise ("Invalid Credentials!")

    def getPipeLine(self, sourceLanguage, targetLanguage):
        ulcaEndPoint = (
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        )
        requestPayload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": sourceLanguage,
                            "targetLanguage": targetLanguage,
                        },
                    },
                },
            ],
            "pipelineRequestConfig": {
                "pipelineId": "64392f96daac500b55c543cd",
            },
        }
        response = requests.post(
            ulcaEndPoint,
            data=json.dumps(requestPayload),
            headers={
                "ulcaApiKey": self.ulcaApiKey,
                "userID": self.ulcaUserId,
                "Content-Type": "application/json",
            },
        )

        self.pipeLineData = response.json()
