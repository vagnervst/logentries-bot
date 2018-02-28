from logentriesbot.bots.bot import Bot
from logentriesbot.client.logentries import post_query, get_timestamp
from logentriesbot.monitoring import add_company, remove_company


class LogWatcher(Bot):
    def __init__(self, bot_name, slack_connection):
        Bot.__init__(self, bot_name, slack_connection)

        self.commands = {
            "add": {
                "fn": self.add,
                "required_params": ["company_id", "status_code", "error_message", "quantity", "unit"],
                "async": True
            },
            "remove": {
                "fn": self.remove,
                "required_params": ["job_id"],
                "async": True
            },
            "jump": {
                "fn": self.jump
            },
            "exec": {
                "fn": self.exec
            },
            "help": {
                "fn": self.help
            }
        }

    def jump(self, params=None):
        return "Kris Kross will make you jump jump"

    def add(self, params, callback):
        for c in params:
            if c['name'] == 'company_id':
                company_id = c['value']
            elif c['name'] == 'status_code':
                status_code = int(c['value'])
            elif c['name'] == 'error_message':
                error_message = c['value']
            elif c['name'] == 'quantity':
                quantity = int(c['value'])
            elif c['name'] == 'unit':
                unit = c['value']
        try:
            return add_company(company_id, quantity, unit, callback, status_code, error_message)
        except:
            print("Missing one or more parameters! Check and try again!")

    def remove(self, params, callback):
        for c in params:
            if c['name'] == "job_id":
                job_id = c['value']

        return remove_company(job_id, callback)

    def exec(self, params):
        for c in params:
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
