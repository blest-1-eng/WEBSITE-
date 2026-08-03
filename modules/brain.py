from modules.phone import phone_command
from modules.app_launcher import launch_app
from modules.search import search_web
from modules.planner import plan
from modules.study import (
    study_start,
    study_stop,
    study_status
)
from modules.guardian import (
    guardian_on,
    guardian_off,
    guardian_status,
    set_exam,
    set_goal
)
from modules.ai import ask_ai
from modules.camera import capture_image
from modules.vision import analyze_image
from modules.calculator import calculate
from modules.notes import add_note, get_notes
from modules.memory import remember, recall, all_memory
from modules.memory_ai_v2 import smart_memory
from modules.reminder import set_reminder
from modules.phone import phone_command
from config import USER_NAME
from datetime import datetime


def reply(command):
    original_command = command.strip()
    command = command.lower().strip()

    memory = smart_memory(original_command)

    if memory:
        return memory

    if command == "hi":
        return "Hello How Can I help You Today !😊"

    if command == "time":
        return datetime.now().strftime("%I:%M %p")

    if command == "date":
        return datetime.now().strftime("%d-%m-%Y")

    if command == "help":
        return """
Available Commands
------------------
hi
time
date
help
remember <key> is <value>
what is <key>
note <text>
show notes
calculate <expression>
remind <seconds> <message>

Phone Commands
--------------
battery
location
camera
open browser
torch on
torch off

bye
"""

    if command.startswith("remember "):
        try:
            text = command[9:]
            key, value = text.split(" is ", 1)
            remember(key.strip(), value.strip())
            return "Okay! I'll remember that."
        except:
            return "Use: remember <thing> is <value>"

    if command.startswith("what is "):
        key = command[8:].strip()

        # Remove unnecessary words
        key = key.replace("my ", "")
        key = key.replace("the ", "")
        key = key.strip()

        answer = recall(key)

        if answer:
            return f"Your {key} is {answer}."

        return ask_ai(original_command)

    if command.startswith("note "):
        note = original_command[5:].strip()
        add_note(note)
        return "Note saved successfully."

    if command == "show notes":
        return get_notes()

    if command.startswith("calculate "):
        expression = original_command[10:].strip()
        return calculate(expression)

    if command.startswith("remind "):
        try:
            parts = original_command.split(" ", 2)
            seconds = int(parts[1])
            message = parts[2]
            set_reminder(seconds, message)
            return f"Reminder set for {seconds} seconds."
        except:
            return "Use: remind <seconds> <message>"

    # Guardian Mode

    if command == "guardian on":
        guardian_on()
        return "Guardian Mode Enabled 🛡️"

    if command == "guardian off":
        guardian_off()
        return "Guardian Mode Disabled."

    if command == "guardian status":
        return guardian_status()

    if command.startswith("exam "):
        exam = original_command.replace("exam ", "", 1).strip()
        set_exam(exam)
        return f"Exam saved: {exam}"

    if command.startswith("study goal "):
        try:
            hours = int(command.replace("study goal ", ""))
            set_goal(hours)
            return f"Study goal set to {hours} hours."
        except:
            return "Use: study goal <hours>"

    # Study Tracker

    if command == "study start":
        return study_start()

    if command == "study stop":
        return study_stop()

    if command == "study status":
        return study_status()

    # Open Any App
    if command.startswith("open "):
        app = original_command[5:].strip()
        return launch_app(app)

    # Phone Controls
    phone = phone_command(command)
    if phone is not None:
        return phone

    # Exit
    if command == "bye":
        if USER_NAME.strip():
            return f"Goodbye {USER_NAME}! 👋"

        return "Goodbye! 👋"

    # Web Search

    if command.startswith("search "):

        query = original_command[7:].strip()

        return search_web(query)

    # AI Intent Detection

    intent = plan(original_command)

    if intent["intent"] == "vision":

        print("📷 Opening camera...")

        image = capture_image()

        return analyze_image(image)

    if (
        "ye kya hai" in command
        or "what is this" in command
        or "isko dekh" in command
        or "can you see this" in command
    ):

        image = capture_image()

        return analyze_image(image)

    if intent["intent"] == "guardian_on":
        guardian_on()
        return "Guardian Mode Enabled 🛡️"

    if intent["intent"] == "guardian_off":
        guardian_off()
        return "Guardian Mode Disabled."

    if intent["intent"] == "guardian_status":
        return guardian_status()

    if intent["intent"] == "battery":
        return phone_command("battery")

    if intent["intent"] == "location":
        return phone_command("location")

    if intent["intent"] == "camera":
        return phone_command("camera")

    if intent["intent"] == "browser":
        return phone_command("open browser")

    if intent["intent"] == "torch_on":
        return phone_command("torch on")

    if intent["intent"] == "torch_off":
        return phone_command("torch off")

    if intent["intent"] == "search":
        query = intent.get("query", original_command)
        return search_web(query)

    if intent["intent"] == "bye":
        if USER_NAME.strip():
            return f"Goodbye {USER_NAME}! 👋"

        return "Goodbye! 👋"

    if intent["intent"] == "chat":
        return ask_ai(original_command)

    # AI
    return ask_ai(original_command)
