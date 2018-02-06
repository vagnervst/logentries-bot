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
        #look for '--parameter value' pattern
        foundParams = re.findall(r'--\w+\s+\w+', command)
        parsedParams = []

        for parameter in foundParams:
            paramAndValue = parameter.split(' ')
            mapped = {
                'name': paramAndValue[0][2:],
                'value': paramAndValue[1]
            }

            parsedParams.append(mapped)

        return parsedParams
