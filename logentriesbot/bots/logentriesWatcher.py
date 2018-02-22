from logentriesbot.bots.bot import Bot
from logentriesbot.client.logentries import post_query, get_timestamp
from logentriesbot.monitoring import check, add_company


class LogWatcher(Bot):
    def __init__(self, bot_name, slack_connection):
        Bot.__init__(self, bot_name, slack_connection)

        self.commands = {
            "add": self.add,
            "jump": self.jump,
            "exec": self.exec,
            "check": self.check,
            "help": self.help,
        }

    def jump(self, params=None):
        return "Kris Kross will make you jump jump"

    def check(self, command):
        for c in command:
            if c['name'] == 'id':
                company_id = c['value']
            if c['name'] == 'quantity':
                quantity = int(c['value'])
            if c['name'] == 'unit':
                unit = c['value']

        return check(company_id, quantity, unit)

    def add(self, command, callback):
        for c in command:
            if c['name'] == 'id':
                company_id = c['value']
            if c['name'] == 'quantity':
                quantity = int(c['value'])
            if c['name'] == 'unit':
                unit = c['value']

        return add_company(company_id, quantity, unit, callback)

    def exec(self, command):
        for c in command:
            if c['name'] == 'query':
                statement = c['value']
            elif c['name'] == 'from':
                from_time = get_timestamp(c['value'])
            elif c['name'] == 'to':
                to_time = get_timestamp(c['value'])

        return post_query(statement, from_time, to_time)

    def help(self, params=None):
        response = "Currently I support the following commands:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response
