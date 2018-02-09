import json
from datetime import datetime
from prettyconf import config
import requests


def get_timestamp(dt):
    dt_obj = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S,%f')
    millisec = int(dt_obj.timestamp() * 1000)
    return millisec


def fetch_results(provided_url):
    try:
        response = requests.get(provided_url, headers={'x-api-key': config('LOGENTRIES_API_KEY')})
        return response
    except requests.exceptions.RequestException as error:
        print(error)


def get_all_live_environment():
    all_live_environment_id = 'acd35399-1eb3-45f2-a79e-701b9733a50c'
    all_live_environment_request = fetch_results("https://rest.logentries.com/management/logsets/{0}".format(all_live_environment_id)).json()
    all_live_environment = []
    for log in all_live_environment_request['logset']['logs_info']:
        all_live_environment.append(log['id'])
    return all_live_environment


def get_all_test_environment():
    all_test_environment_id = 'a908909c-9217-4feb-83b7-0ed4798fca3a'
    all_test_environment_request = fetch_results("https://rest.logentries.com/management/logsets/{0}".format(all_test_environment_id)).json()
    all_test_environment = []
    for log in all_test_environment_request['logset']['logs_info']:
        all_test_environment.append(log['id'])
    return all_test_environment


def post_query(statement=None, from_time=None, to_time=None):
    body = {"logs": get_all_test_environment() + get_all_live_environment(),
            "leql": {"during": {"from": from_time, "to": to_time}, "statement": statement}}
    uri = 'https://rest.logentries.com/query/logs/'
    headers = {'x-api-key': config('LOGENTRIES_API_KEY')}

    response = requests.post(uri, json=body, headers=headers)

    while response.status_code >= 200:
        if 'links' in response.json():
            continue_url = response.json()['links'][0]['href']
            response = requests.get(continue_url, headers={'x-api-key': config('LOGENTRIES_API_KEY')})
        else:
            return json.dumps(response.json(), indent=4)


if __name__ == '__main__':
    query = "where(statusCode=400) groupby(name) calculate(count)"
    from_time = get_timestamp("08/02/2018 09:00:00,00")
    to_time = get_timestamp("08/02/2018 09:30:00,00")
    post_query(query, from_time, to_time)
