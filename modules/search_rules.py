IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp",
    ".gif", ".webp", ".tiff", ".ico"
}

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi",
    ".mov", ".wmv", ".flv"
}

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".aac",
    ".ogg", ".flac", ".m4a"
}

DOCUMENT_EXTENSIONS = {
    ".pdf", ".docx", ".doc",
    ".ppt", ".pptx",
    ".xls", ".xlsx",
    ".txt"
}

CODE_EXTENSIONS = {
    ".py", ".cpp", ".c",
    ".java", ".js",
    ".html", ".css",
    ".json", ".xml"
}


def get_category(extension):

    extension = extension.lower()

    if extension in IMAGE_EXTENSIONS:
        return "image"

    if extension in VIDEO_EXTENSIONS:
        return "video"

    if extension in AUDIO_EXTENSIONS:
        return "audio"

    if extension in DOCUMENT_EXTENSIONS:
        return "document"

    if extension in CODE_EXTENSIONS:
        return "code"

    return "other"