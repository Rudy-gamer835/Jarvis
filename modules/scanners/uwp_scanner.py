import subprocess
import json


def scan_uwp():
    """
    Scan Microsoft Store (UWP) applications using Get-StartApps.
    """

    apps = {}

    command = [
        "powershell",
        "-Command",
        "Get-StartApps | Select-Object Name,AppID | ConvertTo-Json"
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return apps

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            data = [data]

        for item in data:

            name = item.get("Name", "").strip()

            appid = item.get("AppID", "").strip()

            if not name:
                continue

            apps[name.lower()] = {
                "name": name,
                "type": "uwp",
                "path": "",
                "appid": appid,
                "install_location": "",
                "aliases": []
            }

    except Exception as e:
        print(e)

    return apps


if __name__ == "__main__":

    apps = scan_uwp()

    print(f"Found {len(apps)} UWP applications\n")

    for app in sorted(apps)[:30]:
        print(app)