import os
import tempfile
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoURL(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    format_id: str
    type: str

@app.post("/api/video-info")
async def get_video_info(data: VideoURL):
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=False)
            
            formats = []
            seen = set()
            
            for f in info.get("formats", []):
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    height = f.get("height") or 0
                    if height > 0 and height not in seen:
                        seen.add(height)
                        formats.append({
                            "format_id": f.get("format_id"),
                            "resolution": f"{height}p",
                            "ext": f.get("ext", "mp4"),
                            "filesize": round((f.get("filesize") or 0) / (1024*1024), 1) or None,
                            "fps": f.get("fps"),
                            "type": "progressive"
                        })
            
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
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/download")
async def download_video(data: DownloadRequest):
    temp_dir = tempfile.mkdtemp()
    
    try:
        ydl_opts = {
            "quiet": True,
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        }
        
        if data.type == "audio_only":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }]
        elif data.type == "progressive":
            ydl_opts["format"] = data.format_id
        else:
            ydl_opts["format"] = f"{data.format_id}+bestaudio/best"
            ydl_opts["merge_output_format"] = "mp4"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            filename = ydl.prepare_filename(info)
            
            if data.type == "audio_only":
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            
            if not os.path.exists(filename):
                raise HTTPException(status_code=500, detail="Download failed")
            
            return FileResponse(
                path=filename,
                filename=os.path.basename(filename),
                media_type="application/octet-stream",
                background=lambda: shutil.rmtree(temp_dir, ignore_errors=True)
            )
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=400, detail=str(e))
