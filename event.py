from command import Command
from commandParser import CommandParser

class Event:
    def __init__(self, bot):
        self.bot = bot
        self.command = Command()


    def wait_for_event(self):
        events = self.bot.slack_client.rtm_read()

        if events and len(events) > 0:
            for event in events:
                self.parse_event(event)


    def parse_event(self, event):

        if event.get('type') == 'message' and self.bot.bot_id in event['text']:
            commandFromUser = event['text'].split(self.bot.bot_id)[1].strip().lower()

            command = CommandParser(commandFromUser)
            self.handle_event(event['user'], command, event['channel'])

    def handle_event(self, user, command, channel):
        if command and channel:
            print("Received command: " + command.name + " in channel: " + channel + " from user: " + user)
            if command.parameters:
                print("Parameters used: " + command.join_parameters())

            response = self.command.handle_command(user, command.name)
            self.bot.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
