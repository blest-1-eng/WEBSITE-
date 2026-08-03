import subprocess

def listen():
    try:
        result = subprocess.check_output(
            ["termux-speech-to-text"],
            text=True
        ).strip()

        return result

    except Exception:
        return ""
