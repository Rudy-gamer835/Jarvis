from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "jarvis.log"


def _write(level, message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] [{level}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line)


def info(message):

    console.print(f"[cyan][INFO][/cyan] {message}")

    _write("INFO", message)


def success(message):

    console.print(f"[green][SUCCESS][/green] {message}")

    _write("SUCCESS", message)


def warning(message):

    console.print(f"[yellow][WARNING][/yellow] {message}")

    _write("WARNING", message)


def error(message):

    console.print(f"[bold red][ERROR][/bold red] {message}")

    _write("ERROR", message)

if __name__ == "__main__":

    info("Jarvis started")

    success("Application database loaded")

    warning("Spotify not found")

    error("Chrome failed to launch")