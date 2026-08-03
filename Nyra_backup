from modules.brain import reply
from modules.voice import speak

print("=" * 45)
print("🤖 Hey Akshat, Nyra is here.")
print("Type 'help' to see commands.")
print("=" * 45)

while True:
    command = input("\nYou: ")

    response = reply(command)

    print("Nyra:", response)
    speak(response)

    if command.lower() == "bye":
        break
