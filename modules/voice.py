import subprocess
import re

VOICE = "hi-IN-SwaraNeural"


def clean_text(text):
    # Emojis aur special Unicode remove karega
    return re.sub(r"[^\x00-\x7F]+", "", text)


def speak(text):
    filename = "nyra.mp3"

    # Voice ke liye emojis remove
    text = clean_text(text)

    try:
        # MP3 generate
        subprocess.run([
            "edge-tts",
            "--voice", VOICE,
            "--text", text,
            "--write-media", filename
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Play audio
        subprocess.run([
            "termux-media-player",
            "play",
            filename
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception as e:
        print("Voice Error:", e)
