from slackclient import SlackClient


class SlackConnection(object):

    def __init__(self, token):
        self.slack_client = SlackClient(token)
        self.attached_bots = []

    def attach_bot(self, bot):
        bot_id = self.get_bot_id(bot.name)

        if bot_id is None:
            raise Exception('SlackConnection', 'Bot name not found')

        self.attached_bots.append(bot)

    def get_bot_id(self, bot_name):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == bot_name:
                    return "<@" + user.get('id') + ">"

            return None

    def get_attached_bot(self, bot_id):

        for bot in self.attached_bots:
            if bot_id == bot.id:
                return bot

        return None


class SlackAttachment(object):

    def __init__(self, color_hex):
        self._attachment = {
            "color": color_hex,
            "fields": [],
            "actions": []
        }

    def field(self, **kwargs):
        new_field = {
            "title": kwargs["title"],
            "value": kwargs["value"],
            "short": kwargs["short"]
        }

        self._attachment["fields"].append(new_field)
        return self

    def action(self, **kwargs):
        new_action = {
            "name": kwargs["name"],
            "text": kwargs["text"],
            "type": kwargs["type"],
            "url": kwargs["url"]
        }

        self._attachment["actions"].append(new_action)
        return self

    def build(self):
        return self._attachment
