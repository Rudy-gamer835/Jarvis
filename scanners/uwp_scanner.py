import subprocess
import json


def scan_uwp():
    """
    Scan installed Microsoft Store (UWP) apps.

    Returns:
        {
            "calculator": {
                "name": "Calculator",
                "path": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
                "type": "uwp"
            },
            ...
        }
    """

    command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command",
        "Get-StartApps | Select-Object Name, AppID | ConvertTo-Json -Depth 2"
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace"
        )

        if result.returncode != 0:
            print(result.stderr)
            return {}

        if not result.stdout.strip():
            return {}

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            data = [data]

        apps = {}

        for app in data:

            name = app.get("Name", "").strip()
            appid = app.get("AppID", "").strip()

            if not name or not appid:
                continue

            key = name.lower().strip()

            apps[key] = {
                "name": name,
                "path": "",
                "appid": appid,
                "type": "uwp"
            }

        return apps

    except Exception as e:
        print("UWP Scanner Error:", e)
        return {}


if __name__ == "__main__":

    apps = scan_uwp()

    print(f"\nFound {len(apps)} UWP Apps\n")

    print("-" * 70)

    for name in sorted(apps):
        print(f"{apps[name]['name']:<40} {apps[name]['path']}")