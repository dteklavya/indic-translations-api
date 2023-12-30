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

    def __init__(self, sourceLanguage, targetLanguage) -> None:
        self.ulcaUserId = os.environ.get("userID")
        self.ulcaApiKey = os.environ.get("ulcaApiKey")
        if not self.ulcaUserId or not self.ulcaApiKey:
            raise ("Invalid Credentials!")
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage

    def getPipeLine(self) -> None:
        ulcaEndPoint = (
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        )
        requestPayload = json.dumps(
            {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": self.sourceLanguage,
                                "targetLanguage": self.targetLanguage,
                            },
                        },
                    },
                ],
                "pipelineRequestConfig": {
                    "pipelineId": "64392f96daac500b55c543cd",
                },
            }
        )
        response = requests.post(
            ulcaEndPoint,
            data=requestPayload,
            headers={
                "ulcaApiKey": self.ulcaApiKey,
                "userID": self.ulcaUserId,
                "Content-Type": "application/json",
            },
        )

        self.pipeLineData = response.json()

    def translate(self, text) -> json:
        if not self.pipeLineData:
            raise "Pipe Line data is not available"

        callbackUrl = self.pipeLineData.get("pipelineInferenceAPIEndPoint").get(
            "callbackUrl"
        )
        inferenceApiKey = (
            self.pipeLineData.get("pipelineInferenceAPIEndPoint")
            .get("inferenceApiKey")
            .get("value")
        )
        serviceId = (
            self.pipeLineData.get("pipelineResponseConfig")[0]
            .get("config")[0]
            .get("serviceId")
        )

        headers = {
            "Authorization": inferenceApiKey,
            "Content-Type": "application/json",
        }
        inputArrayOfDicts = [{"source": i} for i in text.split()]
        requestPayload = json.dumps(
            {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": self.sourceLanguage,
                                "targetLanguage": self.targetLanguage,
                            },
                            "serviceId": serviceId,
                        },
                    },
                ],
                "inputData": {"input": inputArrayOfDicts},
            }
        )
        try:
            response = requests.post(callbackUrl, data=requestPayload, headers=headers)
        except Exception as e:
            raise e
        return response.json().get("pipelineResponse")[0]["output"]
