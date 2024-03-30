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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def asr(request):
    """Automatic Speech recognition - returns text given base64 encoded audio data."""
    sourceLanguage = request.data.get("sourceLanguage")
    base64String = request.data.get("base64String")

    translator = Bhashini(sourceLanguage)
    text = translator.asr(base64String)
    return Response(text)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def asr_nmt(request):
    """
    Given a base64 encoded audio, auto-recognizes source language
    and converts it to text - in the given target language.
    """
    sourceLanguage = request.data.get("sourceLanguage")
    targetLanguage = request.data.get("targetLanguage")
    base64String = request.data.get("base64String")

    translator = Bhashini(sourceLanguage, targetLanguage)
    text = translator.asr_nmt(base64String)
    return Response(text)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def nmt_tts(request):
    sourceLanguage = request.data.get("sourceLanguage")
    targetLanguage = request.data.get("targetLanguage")
    text = request.data.get("text")
    gender = request.data.get("gender")
    translator = Bhashini(sourceLanguage, targetLanguage)

    base64String = translator.nmt_tts(text)
    decodedData = base64.b64decode(base64String)

    buffer = BytesIO()
    buffer.write(decodedData)
    wav_file = "/tmp/nmt_tts.wav"
    with open(wav_file, "wb") as outfile:
        outfile.write(buffer.getbuffer())

    # TODO: Get this to S3 and send back link as response
    buffer.seek(0)
    return FileResponse(buffer, filename=wav_file, as_attachment=True)
