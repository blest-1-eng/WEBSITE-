from modules.intent import detect_intent

while True:

    text = input("> ")

    print(detect_intent(text))
