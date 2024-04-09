"""serializers.py: Validation of input data."""

__author__ = "Rajesh Pethe"
__date__ = "04/09/2024 16:02:56"
__credits__ = ["Rajesh Pethe"]


from rest_framework import serializers
from base64 import b64encode, b64decode


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

    def validate(self, attrs):
        b64str = attrs.get("base64String")
        if not b64str or b64encode(b64decode(b64str)) != b64str.encode("ascii"):
            raise serializers.ValidationError(
                "Ensure this field is a base 64 encoded string."
            )
        return super().validate(attrs)


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
