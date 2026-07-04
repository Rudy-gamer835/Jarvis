import json
from pathlib import Path

from scanners.shortcut_scanner import scan_shortcuts
from scanners.exe_scanner import scan_program_files
from scanners.registry_scanner import scan_registry
from scanners.uwp_scanner import scan_uwp


DATA_DIR = Path("data")
DB_FILE = DATA_DIR / "apps.json"


# Priority:
# shortcut > uwp > desktop > registry
PRIORITY = {
    "shortcut": 4,
    "uwp": 3,
    "desktop": 2,
    "registry": 1
}


def merge_apps(*sources):
    """
    Merge all scanner results into one database.
    Higher-priority entries replace lower-priority ones.
    """

    merged = {}

    for source in sources:

        for key, app in source.items():

            key = key.lower().strip()

            if key not in merged:
                merged[key] = app
                continue

            current = merged[key]

            if PRIORITY[app["type"]] > PRIORITY[current["type"]]:
                merged[key] = app

    return merged


def refresh_database():

    print("\n========== SCANNING APPLICATIONS ==========\n")

    shortcuts = scan_shortcuts()
    print(f"Shortcuts : {len(shortcuts)}")

    exe_apps = scan_program_files()
    print(f"Desktop   : {len(exe_apps)}")

    registry = scan_registry()
    print(f"Registry  : {len(registry)}")

    uwp = scan_uwp()
    print(f"UWP Apps  : {len(uwp)}")

    apps = merge_apps(
        registry,
        exe_apps,
        uwp,
        shortcuts
    )

    DATA_DIR.mkdir(exist_ok=True)

    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(
            dict(sorted(apps.items())),
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n==========================================")
    print(f"Total Unique Apps : {len(apps)}")
    print("Database Saved Successfully")
    print("==========================================\n")

    return apps


def load_apps():

    if not DB_FILE.exists():
        return refresh_database()

    with open(DB_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    refresh_database()