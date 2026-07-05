import os
from pathlib import Path

from core.database import (
    get_connection,
    initialize_database
)

from core.search_rules import get_category
from core.keyword_generator import generate_keywords

# Folders to skip
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
    drives = []

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = Path(f"{letter}:\\")
        if drive.exists():
            drives.append(drive)

    return drives


def scan_drive(drive: Path):

    conn = get_connection()
    cursor = conn.cursor()

    batch = []

    total = 0

    print(f"\nScanning {drive}...\n")

    for root, dirs, files in os.walk(drive, topdown=True):

        dirs[:] = [
            d for d in dirs
            if d not in SKIP_FOLDERS
            and not d.startswith("$")
            and not d.startswith(".")
        ]

        for file in files:

            try:

                full_path = Path(root) / file

                stat = full_path.stat()

                extension = full_path.suffix.lower()

                category = get_category(extension)

                parent_folder = full_path.parent.name

                keywords = generate_keywords(
                    str(full_path),
                    category
                )

                batch.append((
                    file,
                    str(full_path),
                    extension,
                    stat.st_size,
                    stat.st_mtime,
                    drive.drive,
                    str(full_path.parent),
                    parent_folder,
                    category,
                    keywords
                ))

                total += 1

                if len(batch) >= 1000:

                    cursor.executemany("""
                        INSERT OR REPLACE INTO files
                        (
                            name,
                            path,
                            extension,
                            size,
                            modified,
                            drive,
                            folder,
                            parent_folder,
                            category,
                            keywords
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, batch)

                    conn.commit()

                    batch.clear()

                    print(f"Indexed {total:,} files...")

            except (
                PermissionError,
                FileNotFoundError,
                OSError
            ):
                continue

    if batch:

        cursor.executemany("""
            INSERT OR REPLACE INTO files
            (
                name,
                path,
                extension,
                size,
                modified,
                drive,
                folder,
                parent_folder,
                category,
                keywords
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)

        conn.commit()

    conn.close()

    print(f"\nFinished scanning {drive}")
    print(f"Total indexed: {total:,} files")


def scan_all_drives():

    initialize_database()

    drives = get_drives()

    print("\nDetected Drives:\n")

    for drive in drives:
        print(f"• {drive}")

    print()

    for drive in drives:
        scan_drive(drive)

    print("\n===================================")
    print(" JARVIS FILE SCAN COMPLETED ")
    print("===================================")


if __name__ == "__main__":
    scan_all_drives()