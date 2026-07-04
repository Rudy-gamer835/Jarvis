import os
import subprocess

from modules.app_search import find_app


def open_app(command: str) -> str:
    """
    Search and launch an application.
    """

    # Remove "open" if present
    query = command.lower().replace("open", "").strip()

    app = find_app(query)

    if app is None:
        return f"Application '{query}' not found."

    name = app["name"]
    app_type = app["type"]

    try:

        # ---------------- Shortcut ----------------
        if app_type == "shortcut":

            os.startfile(app["path"])
            return f"Opening {name}"

        # ---------------- Desktop EXE ----------------
        elif app_type == "desktop":

            os.startfile(app["path"])
            return f"Opening {name}"

        # ---------------- Registry ----------------
        elif app_type == "registry":

            location = app.get("install_location", "")

            if location and os.path.exists(location):
                os.startfile(location)
                return f"Opening {name}"

            return f"{name} is installed but no launch path is available."

        # ---------------- UWP ----------------
        elif app_type == "uwp":

            appid = app.get("appid", "")

            if appid:
                subprocess.Popen(
                    ["explorer.exe", f"shell:AppsFolder\\{appid}"],
                    shell=False
                )
                return f"Opening {name}"

            return f"{name} has no AppID."

        else:
            return "Unsupported application type."

    except Exception as e:
        return f"Failed to open {name}: {e}"