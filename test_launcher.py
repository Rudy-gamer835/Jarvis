from modules.app_controller import open_app

while True:

    command = input("Open App: ")

    if command.lower() == "exit":
        break

    print(open_app(command))