"""serializers.py: Validation of input data."""

__author__ = "Rajesh Pethe"
__date__ = "04/09/2024 16:02:56"
__credits__ = ["Rajesh Pethe"]


from rest_framework import serializers


class TranslateSerializer(serializers.Serializer):
    sourceLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )
    targetLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )
    text = serializers.CharField()


class TtsSerializer(serializers.Serializer):
    sourceLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )
    text = serializers.CharField()


class AsrSerializer(serializers.Serializer):
    sourceLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )
    base64String = serializers.CharField()


class AsrNmtSerializer(AsrSerializer):
    targetLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )


class NmtTtsSerializer(TtsSerializer):
    targetLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )
    gender = serializers.CharField()


class AsrNmtTtsSerializer(AsrSerializer):
    targetLanguage = serializers.CharField(
        allow_blank=False, min_length=2, max_length=3
    )
    gender = serializers.CharField()
