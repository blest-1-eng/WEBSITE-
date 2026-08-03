import threading
import time

def set_reminder(seconds, message):
    def reminder():
        time.sleep(seconds)
        print(f"\n🔔 Reminder: {message}")

    threading.Thread(target=reminder, daemon=True).start()
