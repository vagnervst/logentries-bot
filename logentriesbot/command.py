import re


class Command(object):

    def __init__(self, commandString):
        self.name = commandString.split(' ')[0].lower()
        self.parameters = self.parse_parameters(commandString)

    def join_parameters(self):
        concat = ""
        for parameter in self.parameters:
            concat += "--" + parameter.get('name') + " " + parameter.get('value') + " "

        return concat

    def parse_parameters(self, command):
        # look for '--parameter "value"' pattern
        foundParams = re.findall(r"(--\w+\s+\"(?:\s?(?:[\w<>=()'\:\/\,]?)\s?)*\")", command)
        parsedParams = []

        for parameter in foundParams:
            param = re.findall(r"--\w+", parameter)[0]
            value = parameter[len(param):].strip().strip("\"")

            mapped = {
                'name': param[2:],
                'value': value
            }

            parsedParams.append(mapped)

        return parsedParams if len(parsedParams) > 0 else None
