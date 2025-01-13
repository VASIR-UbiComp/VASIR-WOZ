from dotenv import find_dotenv, load_dotenv
import requests
import os
from config import OUTPUT_PATH, CHUNK_SIZE
import vlc
import time

load_dotenv()
ELLABS_API_KEY = os.environ.get("ELLABS_API_KEY")
if not ELLABS_API_KEY:
    raise ValueError("ELLABS_API_KEY is not set")

# Headers and data for ElevenLabs API
headers = {"Accept": "application/json", "xi-api-key": ELLABS_API_KEY}

data = {
    "text": "",  # Text you want to convert to speech
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.8,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True,
    },
}

import uuid


def text_to_speech(text, tts_url):
    try:
        unique_filename = f"audio_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(os.path.dirname(OUTPUT_PATH), unique_filename)

        data["text"] = text
        response = requests.post(tts_url, headers=headers, json=data, stream=True)
        if response.ok:
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            print(f"Audio stream saved successfully: {output_path}")
            return output_path
        else:
            print(f"Error in TTS response: {response.text}")
            return None
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None


def play_voice_message(file_path):
    try:
        # Create an instance of the VLC player
        player = vlc.MediaPlayer(file_path)

        # Play the file
        player.play()

        # Wait until the audio is finished playing
        while player.is_playing():
            time.sleep(1)

        print("Playback finished.")

    except Exception as e:
        print(f"Error in play_mp3: {e}")
