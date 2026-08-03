import json
import os
import time

FILE = "data/study.json"


def load_data():
    if not os.path.exists(FILE):
        return {
            "studying": False,
            "start_time": "",
            "today_seconds": 0
        }

    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def study_start():
    data = load_data()

    if data["studying"]:
        return "Study session is already running."

    data["studying"] = True
    data["start_time"] = time.time()

    save_data(data)

    return "Study session started. 📚"


def study_stop():
    data = load_data()

    if not data["studying"]:
        return "No active study session."

    duration = int(time.time() - data["start_time"])

    data["today_seconds"] += duration
    data["studying"] = False
    data["start_time"] = ""

    save_data(data)

    minutes = duration // 60
    hours = minutes // 60
    minutes = minutes % 60

    return f"Study session completed.\nDuration: {hours}h {minutes}m"


def study_status():
    data = load_data()

    total = data["today_seconds"]

    if data["studying"]:
        total += int(time.time() - data["start_time"])

    minutes = total // 60
    hours = minutes // 60
    minutes = minutes % 60

    return f"Today's Study: {hours}h {minutes}m"
