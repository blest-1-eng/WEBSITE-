import json
import os

FILE = "data/guardian.json"


def load_data():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def guardian_on():
    data = load_data()
    data["guardian"] = True
    save_data(data)


def guardian_off():
    data = load_data()
    data["guardian"] = False
    save_data(data)


def guardian_status():
    data = load_data()

    if data.get("guardian"):
        return "Guardian Mode is ON 🛡️"

    return "Guardian Mode is OFF"


def set_exam(date):
    data = load_data()
    data["exam_date"] = date
    save_data(data)


def set_goal(hours):
    data = load_data()
    data["study_goal"] = hours
    save_data(data)


def get_info():
    return load_data()
