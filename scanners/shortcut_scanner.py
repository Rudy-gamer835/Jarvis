from pathlib import Path
import os

START_MENU_PATHS = [
    Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
    Path(os.environ["PROGRAMDATA"]) / "Microsoft/Windows/Start Menu/Programs",
]


def scan_shortcuts():
    """
    Scan Windows Start Menu shortcuts (.lnk)
    Returns:
        dict[str, dict]
    """

    apps = {}

    for base in START_MENU_PATHS:

        if not base.exists():
            continue

        for shortcut in base.rglob("*.lnk"):

            name = shortcut.stem.strip().lower()

            if not name:
                continue

            apps[name] = {
                "name": shortcut.stem.strip(),
                "type": "shortcut",
                "path": str(shortcut),
                "appid": "",
                "install_location": "",
                "aliases": []
            }

    return apps


if __name__ == "__main__":

    apps = scan_shortcuts()

    print(f"Found {len(apps)} shortcuts\n")

    for name in sorted(apps)[:20]:
        print(name)