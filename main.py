from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import subprocess, uuid, requests, os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Video Compressor is running! Paste a video URL at /compress"}

@app.post("/compress")
def compress_video(url: str = Form(...)):
    input_file = f"{uuid.uuid4()}.mp4"
    output_file = f"compressed_{input_file}"

    # Download video
    r = requests.get(url, stream=True)
    with open(input_file, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)

    # Compress with FFmpeg
    subprocess.run([
        "ffmpeg", "-i", input_file,
        "-vcodec", "libx264", "-crf", "28", output_file
    ])

    os.remove(input_file)
    return FileResponse(output_file, filename="compressed.mp4")
