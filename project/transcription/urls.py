# transcription/urls.py
from django.urls import path
from .views import TranscribeAudio  # Import the class, not the function

urlpatterns = [
    path('', TranscribeAudio.as_view(), name='transcribe-audio'),
]