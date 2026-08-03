import subprocess
import difflib


def launch_app(app_name):
    try:
        packages = subprocess.check_output(
            ["cmd", "package", "list", "packages"],
            text=True
        ).splitlines()

        package_map = {}

        for line in packages:
            pkg = line.replace("package:", "").strip()

            # Full package
            package_map[pkg.lower()] = pkg

            # Every part of package
            for part in pkg.lower().split("."):
                if len(part) > 2:
                    package_map[part] = pkg

        # Common aliases
        aliases = {
            "insta": "instagram",
            "ig": "instagram",
            "chrome": "chrome",
            "crome": "chrome",
            "yt": "youtube",
            "playstore": "vending",
            "play store": "vending",
            "reddit": "reddit",
            "telegram": "telegram",
            "snap": "snapchat"
        }

        query = app_name.lower().strip()

        if query in aliases:
            query = aliases[query]

        match = difflib.get_close_matches(
            query,
            package_map.keys(),
            n=1,
            cutoff=0.4
        )

        if not match:
            return "App not found."

        package = package_map[match[0]]

        subprocess.run([
            "monkey",
            "-p",
            package,
            "-c",
            "android.intent.category.LAUNCHER",
            "1"
        ])

        return f"Opening {package}..."

    except Exception as e:
        return f"App Error: {e}"
