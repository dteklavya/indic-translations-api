"""views.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 12:33:48"
__credits__ = ["Rajesh Pethe"]


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from io import BytesIO
from rest_framework.decorators import api_view, permission_classes
from bhashini_translator import Bhashini
import base64


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def translate(request):
    """
    Returns translated text from source to target language.
    """
    sourceLanguage = request.data.get("sourceLanguage")
    targetLanguage = request.data.get("targetLanguage")
    text = request.data.get("text")
    translator = Bhashini(sourceLanguage, targetLanguage)
    return Response(translator.translate(text))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tts(request):
    """
    Returns audio playback for given text.
    """
    sourceLanguage = request.data.get("sourceLanguage")
    text = request.data.get("text")
    translator = Bhashini(sourceLanguage)

    base64String = translator.tts(text)
    decodedData = base64.b64decode(base64String)

    buffer = BytesIO()
    buffer.write(decodedData)
    wav_file = "/tmp/tts.wav"
    with open(wav_file, "wb") as outfile:
        outfile.write(buffer.getbuffer())

    # TODO: Change this to upload audio file to S3 and send back link as response
    buffer.seek(0)
    return FileResponse(buffer, filename=wav_file, as_attachment=True)
