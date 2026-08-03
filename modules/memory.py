import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


MEMORY = load_memory()


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(MEMORY, f, indent=4)


def remember(key, value):
    MEMORY[key.lower()] = value
    save_memory()


def recall(key):
    return MEMORY.get(key.lower())


def all_memory():
    return MEMORY
