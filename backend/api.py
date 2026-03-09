import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
import yt_dlp
import tempfile
import re
from urllib.parse import urlparse, parse_qs
import atexit
import shutil

app = FastAPI()

# CORS configuration for Vercel + Railway
allowed_origins = [
    "http://localhost:3000",  # Local development
    "https://*.vercel.app",   # Vercel deployments
    "https://vercel.app",     # Vercel domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

temp_dirs = []

@atexit.register
def cleanup_temp_dirs():
    for temp_dir in temp_dirs:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except:
            pass

def validate_youtube_url(url: str) -> bool:
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    if not re.match(youtube_regex, url):
        return False
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        return False
    if parsed.hostname not in ['www.youtube.com', 'youtube.com', 'youtu.be', 'm.youtube.com']:
        return False
    return True

def sanitize_filename(filename: str) -> str:
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = filename[:200]
    return filename

class VideoURL(BaseModel):
    url: str
    
    @validator('url')
    def validate_url(cls, v):
        if not validate_youtube_url(v):
            raise ValueError('Invalid YouTube URL')
        if len(v) > 500:
            raise ValueError('URL too long')
        return v

class DownloadRequest(BaseModel):
    url: str
    format_id: str
    type: str
    
    @validator('url')
    def validate_url(cls, v):
        if not validate_youtube_url(v):
            raise ValueError('Invalid YouTube URL')
        if len(v) > 500:
            raise ValueError('URL too long')
        return v
    
    @validator('format_id')
    def validate_format_id(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Invalid format ID')
        return v
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['audio_only', 'progressive', 'video_only']:
            raise ValueError('Invalid type')
        return v

@app.post("/api/video-info")
async def get_video_info(data: VideoURL):
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 10,
            "retries": 3,
            "nocheckcertificate": False,
            "no_color": True,
            "extract_flat": False,
            "age_limit": None
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=False)
            
            formats = []
            seen = set()
            
            # Progressive formats (video+audio)
            for f in info.get("formats", []):
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    height = f.get("height") or 0
                    if height > 0 and height not in seen:
                        seen.add(height)
                        filesize = f.get("filesize") or f.get("filesize_approx") or 0
                        formats.append({
                            "format_id": f.get("format_id"),
                            "resolution": f"{height}p",
                            "ext": f.get("ext", "mp4"),
                            "filesize": round(filesize / (1024*1024), 1) if filesize else None,
                            "fps": f.get("fps"),
                            "type": "progressive"
                        })
            
            # Video-only formats
            seen_vo = set()
            for f in info.get("formats", []):
                if f.get("vcodec") != "none" and f.get("acodec") == "none":
                    height = f.get("height") or 0
                    if height > 0 and height not in seen_vo and height not in seen:
                        seen_vo.add(height)
                        filesize = f.get("filesize") or f.get("filesize_approx") or 0
                        formats.append({
                            "format_id": f.get("format_id"),
                            "resolution": f"{height}p",
                            "ext": f.get("ext", "mp4"),
                            "filesize": round(filesize / (1024*1024), 1) if filesize else None,
                            "fps": f.get("fps"),
                            "type": "video_only"
                        })
            
            # Audio only
            formats.append({
                "format_id": "bestaudio",
                "resolution": "Audio Only",
                "ext": "mp3",
                "filesize": None,
                "type": "audio_only"
            })
            
            formats.sort(key=lambda x: int(x["resolution"].replace("p", "")) if x["resolution"] != "Audio Only" else 0, reverse=True)
            
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "channel": info.get("uploader"),
                "duration": info.get("duration"),
                "formats": formats
            }
    except Exception as e:
        error_msg = str(e)
        if "Failed to resolve" in error_msg or "name resolution" in error_msg:
            raise HTTPException(status_code=503, detail="Network error: Cannot connect to YouTube. Check your internet connection.")
        elif "Video unavailable" in error_msg:
            raise HTTPException(status_code=404, detail="Video not found or unavailable")
        else:
            raise HTTPException(status_code=400, detail=f"Error: {error_msg}")

@app.post("/api/download")
async def download_video(data: DownloadRequest):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        temp_dirs.append(temp_dir)
        
        base_opts = {
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 15,
            "retries": 2,
            "nocheckcertificate": False,
            "no_color": True,
            "max_filesize": 500 * 1024 * 1024,
            "ratelimit": 10 * 1024 * 1024,
            "concurrent_fragment_downloads": 3
        }
        
        if data.type == "audio_only":
            format_str = "bestaudio/best"
            output_template = os.path.join(temp_dir, "video.%(ext)s")
            ydl_opts = {
                **base_opts,
                "format": format_str,
                "outtmpl": output_template,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }]
            }
        elif data.type == "progressive":
            format_str = data.format_id
            output_template = os.path.join(temp_dir, "video.%(ext)s")
            ydl_opts = {
                **base_opts,
                "format": format_str,
                "outtmpl": output_template
            }
        else:
            format_str = f"{data.format_id}+bestaudio/best"
            output_template = os.path.join(temp_dir, "video.%(ext)s")
            ydl_opts = {
                **base_opts,
                "format": format_str,
                "outtmpl": output_template,
                "merge_output_format": "mp4"
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            filename = ydl.prepare_filename(info)
            
            if data.type == "audio_only":
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            
            if not os.path.exists(filename):
                raise HTTPException(status_code=500, detail="Download failed")
            
            file_size = os.path.getsize(filename)
            if file_size > 500 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="File too large")
            
            safe_title = sanitize_filename(info.get('title', 'video'))
            ext = 'mp3' if data.type == 'audio_only' else info.get('ext', 'mp4')
            safe_filename = f"{safe_title}.{ext}"
        
        return FileResponse(
            path=filename,
            filename=safe_filename,
            media_type="application/octet-stream",
            background=lambda: shutil.rmtree(temp_dir, ignore_errors=True) if temp_dir else None
        )
    except HTTPException:
        raise
    except Exception as e:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=400, detail="Download failed")
