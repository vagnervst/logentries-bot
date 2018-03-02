import ast
import json
from datetime import datetime
from datetime import timedelta
from prettyconf import config
import requests


def get_timestamp(dt):
    dt_obj = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
    millisec = int(dt_obj.timestamp() * 1000)
    return millisec


def get_interval_bound(quantity, unit):
    # unit must be: minutes, hours, days or weeks
    kwargs = {unit: quantity}

    to_time = datetime.now()
    from_time = to_time - timedelta(**kwargs)

    from_time = datetime.strftime(from_time, "%d/%m/%Y %H:%M:%S")
    from_time = get_timestamp(from_time)

    return from_time


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


def get_how_many(company_id, from_time, status_code=400):
    statement = "where(statusCode={status_code} AND _id={id} AND /POST/) groupby(_id) calculate(count)".format(status_code=status_code, id=company_id)
    to_time = get_timestamp(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"))

    response = post_query(statement, from_time, to_time)
    response = json.loads(response)

    errors = 0
    if len(response['statistics']['groups']) > 0:
        errors = response['statistics']['groups'][0][company_id]['count']

    result = {
        "errors": errors,
        "query": statement
    }

    return result


def get_how_many_each_error(company_id, from_time, status_code=400):
    statement = "where(statusCode={status_code} AND _id={id} AND /POST/)".format(status_code=status_code, id=company_id)
    to_time = get_timestamp(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"))

    response = post_query(statement, from_time, to_time)
    response = json.loads(response)

    errors = []

    for event in response['events']:
        message = event['message'][1:]
        message = ast.literal_eval(message)

        err_msg = ", "
        errors_messages = []
        for error in message['body']['errors']:
            errors_messages.append(error['message'])
        err_msg = err_msg.join(errors_messages)

        error_added = False
        for error in errors:
            if error['message'] == err_msg:
                error['quantity'] += 1
                error_added = True
        if not error_added:
            errors.append({'message': err_msg, 'quantity': 1})

    return {
        "query": statement,
        "errors": errors
    }


def fetch_results(provided_url):
    try:
        response = requests.get(provided_url, headers={'x-api-key': config('LOGENTRIES_API_KEY')})
        return response
    except requests.exceptions.RequestException as error:
        print(error)


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
