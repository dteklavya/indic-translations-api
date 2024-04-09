"""views.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 12:33:48"
__credits__ = ["Rajesh Pethe"]


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from io import BytesIO
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework import serializers, status
from bhashini_translator import Bhashini
import base64
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    TranslateSerializer,
    TtsSerializer,
    AsrSerializer,
    AsrNmtSerializer,
    NmtTtsSerializer,
    AsrNmtTtsSerializer,
)


@extend_schema(
    request=TranslateSerializer,
    responses={(200, "application/json"): OpenApiTypes.STR},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def translate(request):
    """
    Returns translated text from source to target language.
    """
    serializer = TranslateSerializer(data=request.data)
    if serializer.is_valid():
        sourceLanguage = request.data.get("sourceLanguage")
        targetLanguage = request.data.get("targetLanguage")
        text = request.data.get("text")
        translator = Bhashini(sourceLanguage, targetLanguage)
        return Response(translator.translate(text))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=TtsSerializer,
    responses={(200, "application/octet-stream"): OpenApiTypes.BINARY},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def tts(request):
    """
    Returns audio playback for given text.
    """
    serializer = TtsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@extend_schema(
    request=AsrSerializer,
    responses={(200, "application/json"): OpenApiTypes.STR},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def asr(request):
    """Automatic Speech recognition - returns text given base64 encoded audio data."""

    serializer = AsrSerializer(data=request.data)
    if serializer.is_valid():
        sourceLanguage = request.data.get("sourceLanguage")
        base64String = request.data.get("base64String")

        translator = Bhashini(sourceLanguage)
        text = translator.asr(base64String)
        return Response(text)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=AsrNmtSerializer,
    responses={(200, "application/json"): OpenApiTypes.STR},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def asr_nmt(request):
    """
    Given a base64 encoded audio, auto-recognizes source language
    and converts it to text - in the given target language.
    """
    serializer = AsrNmtSerializer(data=request.data)
    if serializer.is_valid():
        sourceLanguage = request.data.get("sourceLanguage")
        targetLanguage = request.data.get("targetLanguage")
        base64String = request.data.get("base64String")

        translator = Bhashini(sourceLanguage, targetLanguage)
        text = translator.asr_nmt(base64String)
        return Response(text)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=NmtTtsSerializer,
    responses={(200, "application/octet-stream"): OpenApiTypes.BINARY},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def nmt_tts(request):
    """
    Text to speech, with translation to target language.
    """

    serializer = AsrNmtSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@extend_schema(
    request=AsrNmtTtsSerializer,
    responses={(200, "application/octet-stream"): OpenApiTypes.BINARY},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def asr_nmt_tts(request):
    """
    ASR-NMT-TTS (Automatic Speech Recognition - Neural Machine Translation - Text to Speech)
    Automatic Speech recongnition, translation and conversion to audio.
    """

    serializer = AsrNmtTtsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    sourceLanguage = request.data.get("sourceLanguage")
    targetLanguage = request.data.get("targetLanguage")
    base64String = request.data.get("base64String")
    gender = request.data.get("gender")
    translator = Bhashini(sourceLanguage, targetLanguage)

    base64String = translator.asr_nmt_tts(base64String)
    decodedData = base64.b64decode(base64String)

    buffer = BytesIO()
    buffer.write(decodedData)
    wav_file = "/tmp/asr_nmt_tts.wav"
    with open(wav_file, "wb") as outfile:
        outfile.write(buffer.getbuffer())

    # TODO: Get this to S3 and send back link as response
    buffer.seek(0)

    return FileResponse(buffer, filename=wav_file, as_attachment=True)
