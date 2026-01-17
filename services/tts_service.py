from gtts import gTTS
import os
import time


def generate_speech(text):
    tts = gTTS(text)
    timestamp = str(int(time.time()))
    filename = f"speech_{timestamp}.mp3"
    path = os.path.join("static", "audio", filename)

    # Ensure folder exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    tts.save(path)
    return path


