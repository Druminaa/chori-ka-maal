# YouTube Video Downloader

Modern, responsive web application for downloading YouTube videos.

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, yt-dlp

## Features

- 🎨 Modern glassmorphism UI with dark mode
- 📱 Fully responsive design
- 🎬 Video preview with thumbnail
- 📊 Multiple resolution options
- 🎵 Audio-only download
- 📈 Download progress indicator
- ⚡ Fast and efficient

## Setup Instructions

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

## Usage

1. Paste a YouTube URL in the input field
2. Click "Fetch Video Info"
3. Select your preferred quality
4. Click "Download"

## Component Structure

```
frontend/
├── app/
│   ├── page.tsx          # Main page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── Navbar.tsx        # Navigation bar
│   ├── VideoCard.tsx     # Video preview card
│   ├── ResolutionSelector.tsx  # Quality selector
│   ├── DownloadButton.tsx      # Download button
│   └── Footer.tsx        # Footer
```

## API Endpoints

- `POST /api/video-info` - Fetch video metadata
- `POST /api/download` - Download video
