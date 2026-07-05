import os
from pathlib import Path


SKIP_FOLDERS = {
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "$Recycle.Bin",
    "System Volume Information",
    "Recovery",
    "PerfLogs",
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "Temp",
    "Cache",
    "Caches"
}


def get_drives():
    """
    Detect all available drives.
    """

    drives = []

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        drive = Path(f"{letter}:\\")

        if drive.exists():
            drives.append(drive)

    return drives


def scan_folders():
    """
    Scan every folder on every drive.
    """

    folders = {}

    total = 0

    drives = get_drives()

    for drive in drives:

        print(f"\nScanning folders in {drive}")

        for root, dirs, files in os.walk(drive, topdown=True):

            dirs[:] = [
                d for d in dirs
                if d not in SKIP_FOLDERS
                and not d.startswith("$")
                and not d.startswith(".")
            ]

            for folder in dirs:

                try:

                    path = Path(root) / folder

                    key = folder.lower().strip()

                    folders[key] = {

                        "name": folder,

                        "path": str(path),

                        "type": "folder"
                    }

                    total += 1

                    if total % 500 == 0:
                        print(f"Indexed {total:,} folders...")

                except Exception:
                    continue

    print(f"\nTotal folders indexed: {total:,}")

    return folders


if __name__ == "__main__":

    folders = scan_folders()

    print()

    for folder in list(folders.values())[:20]:
        print(folder)