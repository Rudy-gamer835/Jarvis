from pathlib import Path
import os

SEARCH_PATHS = [
    Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")),
    Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")),
]


def scan_program_files():
    """
    Scan Program Files folders for executable applications.
    """

    apps = {}

    for base in SEARCH_PATHS:

        if not base.exists():
            continue

        for exe in base.rglob("*.exe"):

            name = exe.stem.strip().lower()

            if not name:
                continue

            # Ignore uninstallers and helpers
            if name.startswith("unins"):
                continue

            if "uninstall" in name:
                continue

            apps[name] = {
                "name": exe.stem.strip(),
                "type": "desktop",
                "path": str(exe),
                "appid": "",
                "install_location": str(exe.parent),
                "aliases": []
            }

    return apps


if __name__ == "__main__":

    apps = scan_program_files()

    print(f"Found {len(apps)} executables\n")

    for app in sorted(apps)[:20]:
        print(app)