from modules.app_controller import open_app


def route_command(command):

    command = command.lower()

    if command.startswith("open "):

        app = command.replace("open ", "", 1)

        return open_app(app)

    return "Command not recognized."