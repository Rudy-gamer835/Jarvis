from pathlib import Path


FOLDER_ALIASES = {

    "screenshots": [
        "screenshot",
        "screen shot",
        "capture"
    ],

    "captures": [
        "screen recording",
        "recording",
        "video capture"
    ],

    "wallpapers": [
        "wallpaper",
        "background",
        "desktop background"
    ],

    "downloads": [
        "download"
    ],

    "documents": [
        "document",
        "notes",
        "assignment"
    ],

    "music": [
        "song",
        "music",
        "audio"
    ],

    "pictures": [
        "photo",
        "image",
        "picture"
    ]
}


def generate_keywords(path, category):

    p = Path(path)

    words = set()

    words.update(
        p.stem.lower().replace("_", " ").split()
    )

    words.add(category)

    for folder in p.parts:

        folder = folder.lower()

        words.add(folder)

        if folder in FOLDER_ALIASES:

            words.update(
                FOLDER_ALIASES[folder]
            )

    return ",".join(sorted(words))