"""urls.py: """

__author__ = "Rajesh Pethe"
__date__ = "03/09/2024 12:40:00"
__credits__ = ["Rajesh Pethe"]


from django.urls import path
from .views import translate, tts, asr_nmt, asr, nmt_tts, asr_nmt_tts


urlpatterns = [
    path("translate/", translate, name="translate"),
    path("tts/", tts, name="tts"),
    path("asr_nmt/", asr_nmt, name="asr_nmt"),
    path("asr/", asr, name="asr"),
    path("nmt_tts/", nmt_tts, name="nmt_tts"),
    path("asr_nmt_tts/", asr_nmt_tts, name="asr_nmt_tts"),
]
