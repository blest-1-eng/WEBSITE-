from modules.guardian import get_info
from modules.brain import reply
from modules.voice import speak
from modules.listen import listen

print("=" * 45)
print("🤖 Hey Akshat, Nyra is here.")
print("=" * 45)

# Guardian Info
info = get_info()

if info.get("guardian"):

    print("🛡️ Guardian Mode: ON")

    goal = info.get("study_goal", 0)
    done = info.get("study_done", 0)

    if goal > 0:
        print(f"🎯 Today's Goal: {done}/{goal} hours")

    if info.get("exam_date"):
        print(f"📚 Exam: {info['exam_date']}")

print("Type or press Enter to speak.")
print("=" * 45)

while True:

    command = input("\nYou (Press Enter to speak): ")

    if command.strip() == "":

        print("🎤 Listening...")

        command = listen()

        print("You:", command)

    response = reply(command)

    print("Nyra:", response)

    speak(response)

    if command.lower() in ["bye", "goodbye", "exit"]:
        break
