import json
import requests
from datetime import datetime


class LogentriesConnection(object):
    API_URL = "https://rest.logentries.com"

    def __init__(self, key):
        self.key = key

    def get_logset_logs(self, logset_id):
        path = "/management/logsets/{0}".format(logset_id)
        response = self.get(path).json()

        logs = []
        for log in response['logset']['logs_info']:
            logs.append(log['id'])

        return logs

    def _build_headers(self):
        return {'x-api-key': self.key}

    def get(self, path):
        url = "{0}{1}".format(self.API_URL, path)
        response = requests.get(url, headers=self._build_headers())
        return response

    def post(self, path, query):
        headers = self._build_headers()
        path = "{0}{1}".format(self.API_URL, path)

        response = requests.post(
            path,
            json=query,
            headers=headers
        )

        while response.status_code >= 200:
            if 'links' in response.json():
                continue_url = response.json()['links'][0]['href']
                response = requests.get(continue_url, headers=headers)
            else:
                return json.dumps(response.json(), indent=4)

    def query(self, query):
        pass


class Query(object):

    def __init__(self, statement, range, logs):
        self.logs = logs
        self.statement = statement
        self.from_timestamp = range['from']
        self.to_timestamp = range['to']

    def build(self):
        query = {
            "logs": self.logs,
            "leql": {
                "during": {
                    "from": self.from_timestamp,
                    "to": self.to_timestamp
                },
                "statement": self.statement
            }
        }

        return query


def get_timestamp(dt):
    dt_obj = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
    millisec = int(dt_obj.timestamp() * 1000)
    return millisec
