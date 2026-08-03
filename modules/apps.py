import subprocess
import difflib


def open_app(app_name):
    try:
        output = subprocess.check_output(
            ["termux-launcher", "-l"],
            text=True
        )

        apps = {}

        for line in output.splitlines():
            if "|" in line:
                label, package = line.split("|", 1)
                apps[label.lower().strip()] = package.strip()

        if not apps:
            return "No apps found."

        names = list(apps.keys())

        match = difflib.get_close_matches(
            app_name.lower(),
            names,
            n=1,
            cutoff=0.45
        )

        if not match:
            return "I couldn't find that app."

        package = apps[match[0]]

        subprocess.run(
            ["monkey", "-p", package,
             "-c", "android.intent.category.LAUNCHER", "1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return f"Opening {match[0].title()}."

    except Exception as e:
        return str(e)
