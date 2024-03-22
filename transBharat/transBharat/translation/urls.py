"""urls.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 12:40:00"
__credits__ = ["Rajesh Pethe"]


from django.urls import path
from .views import translate, tts, asr_nmt


urlpatterns = [
    path("translate/", translate, name="translate"),
    path("tts/", tts, name="tts"),
    path("asr_nmt/", asr_nmt, name="asr_nmt"),
]
