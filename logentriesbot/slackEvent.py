import time
from prettyconf import config

from logentriesbot.client.slack import SlackConnection
from logentriesbot.bots.logentriesWatcher import LogWatcher


class SlackEvent(object):

    def __init__(self):
        self.client = SlackConnection(config('SLACK_API_TOKEN'))

        logWatcher = LogWatcher('logentries_bot', self.client)
        logWatcher = LogWatcher('supportbot', self.client)

        self.client.attach_bot(logWatcher)

    def listen(self):
        if self.client.slack_client.rtm_connect(with_team_state=False):
            print("Successfully connected, listening for commands")
            while True:
                self.wait_for_event()

                time.sleep(1)
        else:
            exit("Slack RTM connection failed")

    def wait_for_event(self):
        events = self.client.slack_client.rtm_read()

        if events and len(events) > 0:
            for event in events:
                self.parse_event(event)

    def parse_event(self, event):
        if event.get('type') == 'message' and "text" in event:
            mentioned_bot_id = event['text'].split(' ')[0]
            attached_bot = self.client.get_attached_bot(mentioned_bot_id)

            if attached_bot is not None:
                commandFromUser = event['text'].split(mentioned_bot_id)[1]
                commandFromUser = commandFromUser.strip()
                command = attached_bot.get_built_command(commandFromUser)

                if command.async:
                    self.event = event
                    self.handle_event_async(command, attached_bot, self.async_handler)
                else:
                    event_response = self.handle_event(command, attached_bot)
                    message = {
                        'message': event_response,
                        'channel': event['channel'],
                        'user': event['user']
                    }

                    print("Received command: " + command.name + " in channel: " + event.get('channel') + " from user: " + event.get('user'))
                    self.answer(message)

    def async_handler(self, response):
        message = {
            'message': response,
            'channel': self.event['channel'],
            'user': self.event['user']
        }
        self.answer(message)

    def answer(self, message):
        response = "<@" + message['user'] + "> " if message['user'] else ""
        response += message['message']
        self.client.slack_client.api_call("chat.postMessage", channel=message['channel'], text=response, as_user=True)

    def handle_event(self, command, bot):
        if command.parameters:
            print("Parameters used: " + command.join_parameters())

        return bot.handle_command(command)

    def handle_event_async(self, command, bot, callback):
        if command.parameters:
            print("Parameters used: " + command.join_parameters())

        return bot.handle_command_async(command, callback)
