MAX_HISTORY = 10

history = []

def add_message(role, message):
    history.append({
        "role": role,
        "content": message
    })

    if len(history) > MAX_HISTORY:
        history.pop(0)

def get_history():
    return history

def clear_history():
    history.clear()
