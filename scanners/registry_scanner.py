import winreg


REGISTRY_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]


def scan_registry():
    """
    Scan installed applications from Windows Registry.
    """

    apps = {}

    for hive, path in REGISTRY_PATHS:

        try:
            key = winreg.OpenKey(hive, path)
        except FileNotFoundError:
            continue

        count = winreg.QueryInfoKey(key)[0]

        for i in range(count):

            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)

                name = ""
                install_location = ""

                try:
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                except FileNotFoundError:
                    continue

                try:
                    install_location = winreg.QueryValueEx(
                        subkey,
                        "InstallLocation"
                    )[0]
                except FileNotFoundError:
                    install_location = ""

                if not name:
                    continue

                apps[name.lower()] = {
                    "name": name,
                    "type": "registry",
                    "path": "",
                    "appid": "",
                    "install_location": install_location,
                    "aliases": []
                }

            except Exception:
                continue

    return apps


if __name__ == "__main__":

    apps = scan_registry()

    print(f"Found {len(apps)} registry applications\n")

    for app in sorted(apps)[:20]:
        print(app)