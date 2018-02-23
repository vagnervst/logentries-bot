from logentriesbot.command import Command


class Bot(object):
    def __init__(self, bot_name, slack_connection):
        self.name = bot_name
        self.id = slack_connection.get_bot_id(bot_name)
        self.commands = {}

    def handle_command(self, command):
        response = "Sorry I don't understand the command: " + command.name

        if command.name in self.commands:
            response = self.commands[command.name]['fn'](command.parameters)

        return response

    def handle_command_async(self, command, callback):
        response = "Sorry I don't understand the command: " + command.name

        if command.name in self.commands:
            response = self.commands[command.name](command.parameters, callback)

        return response

    def get_command(self, command):
        if command in self.commands:
            command_spec = self.commands[command]
            async = True if 'async' in command_spec else False
            return Command(command, async)

        return None
