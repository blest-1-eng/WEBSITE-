import subprocess


def phone_command(command):
    command = command.lower().strip()

    try:
        # Battery
        if "battery" in command:
            return subprocess.check_output(
                ["termux-battery-status"],
                text=True
            )

        # Location
        elif "location" in command:
            return subprocess.check_output(
                ["termux-location"],
                text=True
            )

        # Camera
        elif "camera" in command:
            subprocess.run([
                "termux-camera-photo",
                "/sdcard/nyra_photo.jpg"
            ])
            return "Photo captured successfully."

        # Browser
        elif "browser" in command or "open browser" in command:
            subprocess.run([
                "termux-open-url",
                "https://www.google.com"
            ])
            return "Opening browser."

        # Torch ON
        elif "torch on" in command:
            subprocess.run([
                "termux-torch",
                "on"
            ])
            return "Torch turned ON."

        # Torch OFF
        elif "torch off" in command:
            subprocess.run([
                "termux-torch",
                "off"
            ])
            return "Torch turned OFF."

        return None

    except Exception as e:
        return f"Phone Error: {e}"
