# Backend API

FastAPI backend for YouTube video downloader.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn api:app --reload --port 8000
```

## Endpoints

- POST `/api/video-info` - Get video metadata
- POST `/api/download` - Download video
