"""views.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 12:33:48"
__credits__ = ["Rajesh Pethe"]


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from bhashini_translator import Bhashini


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def translate(request):
    sourceLanguage = request.data.get("sourceLanguage")
    targetLanguage = request.data.get("targetLanguage")
    text = request.data.get("text")
    translator = Bhashini(sourceLanguage, targetLanguage)
    return Response(translator.translate(text))
