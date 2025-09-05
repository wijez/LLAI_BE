from django.urls import path
from .views import TranscribeAPIView, record_page, TextToSpeechView, tts_test_page

urlpatterns = [
    path('transcribe/', TranscribeAPIView.as_view(), name='transcribe'),
     path("record/", record_page, name="record"), 
     path('tts/', TextToSpeechView.as_view(), name='tts'),
    path("tts-test/", tts_test_page, name="tts_page"), 
]