import os
import whisper
from pyannote.audio import Pipeline
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



class TranscribeAudio(APIView):
    def post(self, request):
        if not request.FILES.get('audio'):
            return Response(
                {"error": "No audio file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        audio_file = request.FILES['audio']
        
        # Save file temporarily using Django's storage API
        temp_path = f"temp_audio/audio_{datetime.now().strftime('%Y%m%d%H%M%S')}_{audio_file.name}"
        saved_path = default_storage.save(temp_path, ContentFile(audio_file.read()))
        
        try:
            # Process audio
            result = self.transcribe_with_diarization(default_storage.path(saved_path))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up temp file
            if default_storage.exists(saved_path):
                default_storage.delete(saved_path)

    def transcribe_with_diarization(self, audio_path):
        """Helper method to handle the transcription process"""
        try:
            # Load models
            model = whisper.load_model("base")
            pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=os.getenv('PYANNOTE_TOKEN')
            )
            
            # Transcribe audio
            result = model.transcribe(audio_path, word_timestamps=True)
            
            # Perform diarization
            diarization = pipeline(audio_path)
            
            # Combine results
            output = []
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                
                # Find speaker for this segment
                speaker = "SPEAKER_UNKNOWN"
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    if turn.start <= start <= turn.end:
                        break
                
                output.append({
                    "start": start,
                    "end": end,
                    "speaker": speaker,
                    "text": text
                })
            
            return {"segments": output}
        
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")