from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import zipfile

app = FastAPI()

# Update VIDEO_DIR to the correct path
VIDEO_DIR = r"D:\Data Raw\TestData"  # Use raw string (r"") to handle backslashes correctly
DOWNLOAD_DIR = "downloads"  # Keep this local, or modify if needed
ZIP_FILE_PATH = os.path.join(DOWNLOAD_DIR, "all_videos.zip")

# Ensure the downloads directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.get("/videos")
def list_videos():
    if not os.path.exists(VIDEO_DIR):
        return {"error": "Video directory not found"}
    files = os.listdir(VIDEO_DIR)
    return {"videos": files}


@app.get("/videos/{filename}")
def download_video(filename: str):
    file_path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/videos/download_all")
def download_all_videos():

    # Ensure video directory exists
    if not os.path.exists(VIDEO_DIR):
        raise HTTPException(status_code=404, detail="Video directory not found")

    video_files = [f for f in os.listdir(VIDEO_DIR) if os.path.isfile(os.path.join(VIDEO_DIR, f))]

    if not video_files:
        raise HTTPException(status_code=404, detail="No videos found to zip")

    # Create a ZIP file containing all videos
    with zipfile.ZipFile(ZIP_FILE_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in video_files:
            file_path = os.path.join(VIDEO_DIR, file)
            zipf.write(file_path, arcname=file)

    # Ensure the file exists before returning it
    if not os.path.exists(ZIP_FILE_PATH):
        raise HTTPException(status_code=500, detail="ZIP file could not be created")

    return FileResponse(ZIP_FILE_PATH, filename="all_videos.zip", media_type="application/zip")

