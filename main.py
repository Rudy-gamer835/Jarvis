from command_router import route_command
from voice_engine import speak
from listener import listen

from rich.console import Console

console = Console()


def keyboard_mode():
    speak("Keyboard mode activated,BOSS")

    while True:
        command = input("You: ")
        print("You:", command)

        if command.lower() == "exit":
            speak("Going back to mode selection, BOSS")
            break

        speak("Processing command,BOSS")
        response = route_command(command)
        print("Jarvis:", response)
        speak(response)


def voice_mode():
    speak("Voice mode activated,BOSS")

    while True:
        command = listen()

        print("You:", command)

        if "exit" in command:
            speak("Going back to mode selection,BOSS")
            break

        speak("Processing command,BOSS")
        response = route_command(command)
        print("Jarvis:", response)
        speak(response)


def main():
    console.print("\n[bold cyan]========================[/bold cyan]")
    console.print("[bold green]      JARVIS SYSTEM[/bold green]")
    console.print("[bold cyan]========================[/bold cyan]\n")

    speak("Hello BOSS,JARVIS is now online and ready for your service")

    while True:
        console.print("\n[bold yellow]Select Mode:[/bold yellow]")
        console.print("[1] Voice Mode")
        console.print("[2] Keyboard Mode")
        console.print("[3] Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            speak("Entering voice mode,BOSS")
            voice_mode()

        elif choice == "2":
            speak("Entering keyboard mode,BOSS")
            keyboard_mode()

        elif choice == "3":
            speak("Bye  BOSS , JARVIS is going for sleep")
            break

        else:
            speak("Invalid option selected")


if __name__ == "__main__":
    main()