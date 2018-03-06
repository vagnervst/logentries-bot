from logentriesbot.bots.bot import Bot
from logentriesbot.client.logentries import LogentriesConnection, Query
from logentriesbot.client.logentrieshelper import LogentriesHelper
from logentriesbot.monitoring import add_company, remove_company, get_jobs
from prettyconf import config


class LogWatcher(Bot):
    def __init__(self, bot_name, slack_connection):
        Bot.__init__(self, bot_name, slack_connection)

        self.commands = {
            "add": {
                "fn": self.add,
                "required_params": [
                    "company_id",
                    "status_code",
                    "error_message",
                    "quantity",
                    "unit"
                ],
                "async": True
            },
            "remove": {
                "fn": self.remove,
                "required_params": ["job_id"],
                "async": True
            },
            "get_jobs": {
                "fn": self.get_jobs,
                "async": True
            },
            "jump": {
                "fn": self.jump
            },
            "query": {
                "fn": self.query
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
            return add_company(
                company_id, quantity, unit,
                callback, status_code, error_message
            )
        except Exception:
            print("Missing one or more parameters! Check and try again!")

    def remove(self, params, callback):
        for c in params:
            if c['name'] == "job_id":
                job_id = c['value']

        return remove_company(job_id, callback)

    def get_jobs(self, params, callback):
        return get_jobs(callback)

    def query(self, params):
        for c in params:
            if c['name'] == 'query':
                statement = c['value']
            elif c['name'] == 'from':
                from_time = LogentriesHelper.get_timestamp(c['value'])
            elif c['name'] == 'to':
                to_time = LogentriesHelper.get_timestamp(c['value'])

        logs = LogentriesHelper.get_all_test_environment()
        + LogentriesHelper.get_all_live_environment()

        query = Query(statement, {
            'from': from_time, 'to': to_time
        }, logs)

        client = LogentriesConnection(config('LOGENTRIES_API_KEY'))
        return client.post('/query/logs', query.build())

    def help(self, params=None):
        response = "Currently I support the following commands:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response
