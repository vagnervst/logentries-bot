from logentriesbot.bots.bot import Bot


class LogWatcher(Bot):
    def __init__(self, bot_name, slack_connection):
        Bot.__init__(self, bot_name, slack_connection)

        self.commands = {
            "jump": self.jump,
            "help": self.help,
            "hello": self.hello
        }

    def jump(self, params=None):
        return "Kris Kross will make you jump jump"

    def help(self, params=None):
        response = "Currently I support the following commands:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response

    def hello(self, params=None):
        return "World!"
