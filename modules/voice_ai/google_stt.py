import speech_recognition as sr

r = sr.Recognizer()

def speech_to_text(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio)

    except Exception:
        return None
