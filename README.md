# live-video-transcript-description

# Introduction
This Streamlit application extracts frames and audio from a live stream URL (YouTube, Twitch, etc.), performs analysis on the extracted frames and audio, and generates a consolidated description based on the video frames and transcript.

# Usage
Clone this repository to your local machine.
Install the required dependencies by running:
```python
pip install -r requirements.txt
```

Set up your environment variables:
OPENAI_API_KEY: Your OpenAI API key.
WHISPER_API_KEY: Your Whisper API key.

Run the application using Streamlit:
```python
streamlit run main.py
```

Enter the live stream URL in the provided text input and select the number of seconds for extraction using the slider.
The application will extract frames and audio, display the frames, and provide a transcript of the audio.
It will then generate descriptions for the frames and a consolidated description based on the transcript and frame descriptions.

# Requirements
Python 3.7 or higher
Streamlit
ffmpeg
OpenAI API key
Whisper API key

```python
streamlit run main.py
```
