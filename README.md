# Darwix AI Technical Assessment

## Project Overview
This Django application demonstrates the integration of AI features including:
1. **Audio Transcription with Speaker Diarization**
2. **AI-Powered Blog Title Suggestions**

Built for the Darwix AI technical evaluation process.

## Features Implemented

### 1. Audio Transcription with Diarization
- Transcribes audio files (WAV/MP3) to text
- Identifies different speakers with timestamps
- Returns structured JSON output
- Supports multilingual audio (automatic language detection)

### 2. AI Blog Title Suggestions
- Generates 3 relevant title suggestions
- Uses GPT-2 medium model for quality outputs
- Processes content in real-time
- Returns JSON formatted suggestions

## Technical Stack
- **Backend**: Django 5.2
- **AI Models**: 
  - Whisper (Audio Transcription)
  - PyAnnote (Speaker Diarization) 
  - GPT-2 Medium (Title Generation)
- **APIs**: RESTful endpoints

## Setup Instructions

### Prerequisites
- Python 3.10+
- FFmpeg (`sudo apt install ffmpeg` or `brew install ffmpeg`)
- PyTorch (will be installed via requirements.txt)

### Installation
```bash
git clone https://github.com/Rahul-web-hub/Darwin-Assignment.git
cd Darwin-Assignment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "PYANNOTE_TOKEN=your_huggingface_token" > .env
echo "DEBUG=True" >> .env
```
# 🧠 AI-Powered Blog & Audio API

This project provides a set of RESTful API endpoints for audio transcription with speaker diarization and intelligent blog title generation. It also includes a simple health check for service status.

---

## 🚀 API Endpoints Documentation

---

### 📌 1. Audio Transcription with Diarization

**Endpoint**: `POST /api/transcribe/`  
**Description**: Transcribes audio files with speaker identification and timing information.

#### 🔸 Request

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@test_audio.wav" \
  http://localhost:8000/api/transcribe/
```

**Parameters**:
- `audio` (required): Audio file (WAV/MP3 format, <10MB)

#### ✅ Success Response (200)

```json
{
  "segments": [
    {
      "start": 0.5,
      "end": 2.3,
      "speaker": "SPEAKER_01",
      "text": "Good morning everyone"
    },
    {
      "start": 2.4,
      "end": 4.1,
      "speaker": "SPEAKER_02",
      "text": "Let's begin the meeting"
    }
  ]
}
```

#### ❌ Error Responses

- `400 Bad Request`: Invalid/missing audio file  
- `413 Payload Too Large`: File exceeds 10MB limit  
- `500 Server Error`: Transcription failure

---

### 📌 2. Blog Title Suggestions

**Endpoint**: `POST /api/suggest-titles/`  
**Description**: Generates 3 relevant title suggestions based on blog content.

#### 🔸 Request

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"content":"How to build AI applications with Python..."}' \
  http://localhost:8000/api/suggest-titles/
```

**Parameters**:
- `content` (required): String with blog content (min 20 chars)

#### ✅ Success Response (200)

```json
{
  "titles": [
    "Building AI Applications with Python: A Complete Guide",
    "10 Python Techniques for Effective AI Development",
    "From Python to AI: Essential Development Strategies"
  ]
}
```

#### ❌ Error Responses

- `400 Bad Request`: Content too short/missing  
- `500 Server Error`: Title generation failure

---

### 📌 3. Health Check (Bonus)

**Endpoint**: `GET /api/health/`  
**Description**: Service status and model loading verification.

#### 🔸 Request

```bash
curl http://localhost:8000/api/health/
```

#### ✅ Success Response (200)

```json
{
  "status": "operational",
  "models_loaded": {
    "transcription": true,
    "diarization": true,
    "title_generation": true
  }
}
```

---

## 📎 Technologies Used

- Python / Django REST Framework
- Whisper / PyAnnote for audio transcription
- OpenAI / LLMs for title generation

---

## 🧪 Local Setup

```bash
git clone https://github.com/your-repo.git
cd your-repo
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

---

## 🛠️ Author & License

**Author**: [Rahul Singh Chauhan](https://github.com/Rahul-web-hub)  
**License**: MIT License
