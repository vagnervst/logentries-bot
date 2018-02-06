import re


class CommandParser(object):

    def __init__(self, command):
        self.name = command.split(' ')[0]
        self.parameters = CommandParser.parse_parameters(command)

    def join_parameters(self):
        concat = ""
        for parameter in self.parameters:
            concat += "--" + parameter.get('name') + " " + parameter.get('value') + " "

        return concat

    def parse_parameters(command):
        # look for '--parameter value' pattern
        foundParams = re.findall(r"(--\w+\s+\"(?:\s?(?:[\w<>=()\:\/\,]?)\s?)*\")", command)
        parsedParams = []

        for parameter in foundParams:
            param = re.findall(r"--\w+", parameter)[0]
            value = parameter[len(param):].strip().strip("\"")

            mapped = {
                'name': param[2:],
                'value': value
            }

            parsedParams.append(mapped)
        return parsedParams
