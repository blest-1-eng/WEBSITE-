import json
import os

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []

NOTES = load_notes()

def add_note(note):
    NOTES.append(note)
    with open(NOTES_FILE, "w") as file:
        json.dump(NOTES, file, indent=4)

def get_notes():
    if not NOTES:
        return "No notes found."

    result = "Your Notes:\n"
    for i, note in enumerate(NOTES, 1):
        result += f"{i}. {note}\n"
    return result
