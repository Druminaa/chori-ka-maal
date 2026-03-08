# #!/usr/bin/env python3
# """
# YouTube Video Downloader
# Requires: pip install yt-dlp
# """

import subprocess
import sys
import json
import os


def install_ytdlp():
    """Install yt-dlp if not already installed."""
    try:
        import yt_dlp
    except ImportError:
        print("Installing yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "-q"])
        print("yt-dlp installed successfully!\n")


def get_available_formats(url):
    """Fetch all available formats for a given YouTube URL."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info


def display_resolutions(formats):
    """Parse and display available video resolutions with audio."""
    print("\n📋 Available Resolutions:\n")
    print(f"{'#':<4} {'Resolution':<15} {'FPS':<6} {'Format':<10} {'Size (approx)':<15} {'Note'}")
    print("-" * 70)

    resolution_options = []
    seen = set()

    # Filter formats with both video and audio (progressive streams)
    progressive = []
    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") != "none":
            height = f.get("height") or 0
            fps = f.get("fps") or 0
            ext = f.get("ext", "?")
            key = (height, ext)
            if key not in seen and height > 0:
                seen.add(key)
                progressive.append(f)

    # Sort by resolution descending
    progressive.sort(key=lambda x: x.get("height", 0), reverse=True)

    # Also collect video-only formats (for merging with audio)
    video_only = []
    seen_vo = set()
    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") == "none":
            height = f.get("height") or 0
            ext = f.get("ext", "?")
            key = (height,)
            if key not in seen_vo and height > 0:
                seen_vo.add(key)
                video_only.append(f)

    video_only.sort(key=lambda x: x.get("height", 0), reverse=True)

    idx = 1

    # Show progressive (video+audio combined)
    for f in progressive:
        height = f.get("height", "?")
        fps = f.get("fps", "?")
        ext = f.get("ext", "?")
        filesize = f.get("filesize") or f.get("filesize_approx")
        size_str = f"{filesize / (1024*1024):.1f} MB" if filesize else "Unknown"
        format_id = f.get("format_id", "")

        print(f"{idx:<4} {str(height)+'p':<15} {str(fps):<6} {ext:<10} {size_str:<15} ✅ Video+Audio")
        resolution_options.append({
            "index": idx,
            "height": height,
            "fps": fps,
            "ext": ext,
            "format_id": format_id,
            "type": "progressive",
            "label": f"{height}p ({ext}) - Video+Audio"
        })
        idx += 1

    # Show video-only (will be merged with best audio)
    for f in video_only:
        height = f.get("height", "?")
        fps = f.get("fps", "?")
        ext = f.get("ext", "?")
        filesize = f.get("filesize") or f.get("filesize_approx")
        size_str = f"{filesize / (1024*1024):.1f} MB" if filesize else "Unknown"
        format_id = f.get("format_id", "")

        print(f"{idx:<4} {str(height)+'p':<15} {str(fps):<6} {ext:<10} {size_str:<15} 🎬 Video + Best Audio (merged)")
        resolution_options.append({
            "index": idx,
            "height": height,
            "fps": fps,
            "ext": ext,
            "format_id": format_id,
            "type": "video_only",
            "label": f"{height}p ({ext}) - Merged"
        })
        idx += 1

    # Audio only option
    print(f"{idx:<4} {'Audio Only':<15} {'-':<6} {'mp3':<10} {'~varies':<15} 🎵 Audio Only (MP3)")
    resolution_options.append({
        "index": idx,
        "type": "audio_only",
        "label": "Audio Only (MP3)"
    })
    idx += 1

    print("-" * 70)
    return resolution_options


def download_video(url, option, output_dir="."):
    """Download the video based on selected option."""
    import yt_dlp

    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    if option["type"] == "audio_only":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    elif option["type"] == "progressive":
        ydl_opts = {
            "format": option["format_id"],
            "outtmpl": output_template,
        }
    else:  # video_only - merge with best audio
        ydl_opts = {
            "format": f"{option['format_id']}+bestaudio/best",
            "outtmpl": output_template,
            "merge_output_format": "mp4",
        }

    print(f"\n⬇️  Downloading: {option['label']}")
    print(f"📁 Saving to: {os.path.abspath(output_dir)}\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    print("=" * 60)
    print("       🎬 YouTube Video Downloader")
    print("=" * 60)

    # Install yt-dlp if needed
    install_ytdlp()

    # Get URL
    url = input("🔗 Enter YouTube URL: ").strip()
    if not url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)

    print("\n🔍 Fetching video information...")

    try:
        info = get_available_formats(url)
    except Exception as e:
        print(f"❌ Error fetching video info: {e}")
        sys.exit(1)

    title = info.get("title", "Unknown Title")
    duration = info.get("duration", 0)
    uploader = info.get("uploader", "Unknown")
    mins, secs = divmod(duration, 60)

    print(f"\n🎥 Title    : {title}")
    print(f"👤 Uploader : {uploader}")
    print(f"⏱️  Duration : {int(mins)}m {int(secs)}s")

    formats = info.get("formats", [])
    options = display_resolutions(formats)

    # Let user pick
    while True:
        try:
            choice = int(input("\n👉 Enter the number of your preferred resolution: "))
            selected = next((o for o in options if o["index"] == choice), None)
            if selected:
                break
            else:
                print(f"⚠️  Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("⚠️  Invalid input. Please enter a number.")

    # Output directory
    out_dir = input("\n📁 Enter download folder (press Enter for current directory): ").strip()
    if not out_dir:
        out_dir = "."

    # Download
    try:
        download_video(url, selected, out_dir)
        print("\n✅ Download complete!")
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        print("💡 Tip: Make sure ffmpeg is installed for merging video+audio formats.")
        print("   Install ffmpeg: https://ffmpeg.org/download.html")


if __name__ == "__main__":
    main()