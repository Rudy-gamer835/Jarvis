from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def banner():
    title = Text("J.A.R.V.I.S SYSTEM ONLINE", style="bold cyan")
    console.print(Panel(title, style="bold blue"))

def show_user(text):
    console.print(f"[bold yellow]You:[/bold yellow] {text}")

def show_jarvis(text):
    console.print(f"[bold green]Jarvis:[/bold green] {text}")

def show_mode(mode):
    console.print(f"[bold magenta]MODE:[/bold magenta] {mode.upper()}")