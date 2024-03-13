##FFMPEG and FASTAPI to extract frames and AUDIO
import subprocess
import streamlink
from fastapi import FastAPI, HTTPException
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
from openai import OpenAI
from pydantic import BaseModel


# Load environment variables
load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
if not OpenAI.api_key:
    raise ValueError("The OpenAI API key must be set in the OPENAI_API_KEY environment variable.")

# Create a FastAPI instance
app = FastAPI()

# Define a Pydantic model to specify the structure of the request body
class StreamURL(BaseModel):
    stream_url: str

# Function to execute FFmpeg command and capture output
def execute_ffmpeg_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("FFmpeg command executed successfully.")
            return result.stdout, result.stderr
        else:
            print("Error executing FFmpeg command:")
            return None, result.stderr
    except Exception as e:
        print("An error occurred during FFmpeg execution:")
        return None, str(e)

# Function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Define FastAPI endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to Live Stream Frame and Audio Extractor API."}

@app.post("/extract")
def extract_frames_and_audio(data: StreamURL):
    print("hello")
    # Fetch the best quality stream URL
    streams = streamlink.streams(data.stream_url)
    if "best" in streams:
        stream_url = streams["best"].url

        # Execute FFmpeg command and capture the output
        ffmpeg_command = [
            'ffmpeg',
            '-i', stream_url,           # Input stream URL
            '-t', '10',                 # Duration to process the input
            '-vf', 'fps=1',             # Extract one frame per second
            '-f', 'image2pipe',         # Output format as image2pipe
            '-c:v', 'mjpeg',            # Codec for output video
            '-an',                      # No audio
            '-'
        ]
        ffmpeg_output, _ = execute_ffmpeg_command(ffmpeg_command)

        if ffmpeg_output:
            frame_list = []

            # Decode frames and store them in a list
            frame_bytes_list = ffmpeg_output.split(b'\xff\xd8')[1:]  # Skip the initial empty frame
            for frame_bytes in frame_bytes_list:
                frame_list.append(image_to_base64(Image.open(BytesIO(b'\xff\xd8' + frame_bytes))))

            # Extract audio
            audio_command = [
                'ffmpeg',
                '-i', stream_url,           # Input stream URL
                '-vn',                      # Ignore the video for the audio output
                '-acodec', 'libmp3lame',    # Set the audio codec to MP3
                '-t', '10',                 # Duration for the audio extraction
                '-f', 'mp3',                # Output format as mp3
                '-'
            ]
            audio_output, _ = execute_ffmpeg_command(audio_command)

            return {"frames": frame_list, "audio": base64.b64encode(audio_output).decode() if audio_output else None}

    else:
        raise HTTPException(status_code=404, detail="No suitable streams found.")

# Run the FastAPI application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)