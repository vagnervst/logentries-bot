from query import post_query, get_timestamp


class Command(object):
    def __init__(self):
        self.commands = {
            "jump": self.jump,
            "exec": self.exec,
            "help": self.help
        }

    def handle_command(self, user, command):
        response = "<@" + user + ">: "

        if command.name in self.commands:
            if command.parameters is None:
                response += self.commands[command.name]()
            else:
                response += self.commands[command.name](command.parameters)
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()

        return response

    def exec(self, command):
        for c in command:
            if c['name'] == 'query':
                statement = c['value']
            elif c['name'] == 'from':
                from_time = c['value']
            elif c['name'] == 'to':
                to_time = c['value']

        result = post_query(statement, from_time, to_time)

    def jump(self, params=None):
        return "Kris Kross will make you jump jump"

    def help(self, params=None):
        response = "Currently I support the following commands:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response
