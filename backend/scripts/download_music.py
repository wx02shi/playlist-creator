import json
import os
import yt_dlp


def download_mp3(youtube_url, output_path):
    # Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_path,
        "force_ipv4": True,
        "quiet": False,
        "no_warnings": False,
        "noplaylist": True,
        "extract_flat": True,
    }

    # Update headers to avoid 403 errors
    yt_dlp.utils.std_headers.update({"User-Agent": "Mozilla/5.0"})

    try:
        print(output_path)
        # Create directory if it doesn't exist
        path = os.path.dirname(output_path)
        os.makedirs(path, exist_ok=True)

        # Download and convert to MP3
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return True
    except Exception as e:
        print(f"Error downloading {youtube_url}: {str(e)}")
        return False


def process_tracks(json_file):
    # Read the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    for track in data["tracks"]:
        youtube_url = track["url"]
        path = "music/" + track["path"]

        if os.path.exists(path):
            continue

        if path.endswith(".mp3"):
            path = path.replace(".mp3", "")
        success = download_mp3(youtube_url, path)

        if success:
            print(f"Successfully downloaded: {track['title']}")
        else:
            print(f"Failed to download: {track['title']}")


if __name__ == "__main__":
    process_tracks("music/tracks.json")
