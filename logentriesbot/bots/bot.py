from logentriesbot.command import Command


class Bot(object):
    def __init__(self, bot_name, slack_connection):
        self.name = bot_name
        self.id = slack_connection.get_bot_id(bot_name)
        self.commands = {}

    def pre_command_handle(self, command):
        pass

    def handle_command(self, command):
        response = "Sorry I don't understand the command: " + command.name

        command_spec = self.get_command(command.name)
        if command_spec is not None:
            command_function = command_spec['fn']
            response = command_function(command.parameters)

        return response

    def handle_command_async(self, command, callback):
        response = "Sorry I don't understand the command: " + command.name

        command_spec = self.get_command(command.name)
        if command_spec is not None:
            command_function = command_spec['fn']
            response = command_function(command.parameters, callback)

        return response

    def get_built_command(self, command):
        command_obj = Command(command, False)
        command_spec = self.get_command(command_obj.name)

        if command_spec is not None:
            command_obj.async = True if 'async' in command_spec else False

        return command_obj

    def get_command(self, command_name):
        command = None

        if command_name in self.commands:
            command = self.commands[command_name]

        return command
