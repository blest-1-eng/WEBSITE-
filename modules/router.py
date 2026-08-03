from modules.intent import detect_intent


def route(command):

    intent = detect_intent(command)

    return intent
