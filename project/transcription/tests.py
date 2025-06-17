# transcription/tests.py
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TranscriptionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.audio_file = SimpleUploadedFile(
            "test.wav",
            b"dummy audio content",  # Replace with real audio bytes if needed
            content_type="audio/wav"
        )

    def test_transcription(self):
        response = self.client.post('/api/transcription/', {'audio': self.audio_file})
        self.assertEqual(response.status_code, 200)
        self.assertIn('segments', response.json())