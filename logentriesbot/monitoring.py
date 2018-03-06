import ast
from apscheduler.schedulers.background import BackgroundScheduler
from logentriesbot.client.logentries import LogentriesConnection, Query
from logentriesbot.client.logentrieshelper import LogentriesHelper, Time
import uuid
from urllib.parse import quote
from datetime import datetime
from prettyconf import config
import json

scheduler = BackgroundScheduler()
scheduler.start()


def check(job_id, company_id, quantity, unit, callback, status_code=400):
    parsed_query_interval = Time.parse(quantity, unit)
    from_time = Time.get_interval_as_timestamp(
        datetime.now(), parsed_query_interval
    )

    errors = get_how_many(company_id, from_time, status_code)

    link = "https://logentries.com/app/73cd17bb#/search/logs/?log_q={}".format(quote(errors["query"]))
    callback("[job_id: *{}*] Company *{}* had *{}* errors in last {} {}! <{}|Run it!>".format(job_id, company_id, errors["errors"], str(quantity), unit, link))


def check_messages(job_id, company_id, quantity, unit, callback, status_code=400):
    from_time = Time.parse(quantity, unit).get_interval_bound(quantity, unit)
    errors = get_how_many_each_error(company_id, from_time, status_code)

    link = "https://logentries.com/app/73cd17bb#/search/logs/?log_q={}".format(quote(errors["query"]))
    if len(errors["errors"]) > 0:
        for e in errors["errors"]:
            callback("[job_id: *{}*] Company *{}* had *{}* errors \"{}\" in last {} {}! <{}|Run it!>".format(job_id, company_id, e['quantity'], e['message'], str(quantity), unit, link))
    else:
        callback("[job_id: *{}*] Company *{}* had *{}* errors in last {} {}! <{}|Run it!>".format(job_id, company_id, 0, str(quantity), unit, link))


def add_company(company_id, quantity, unit, callback, status_code=400, error_message=False):
    global scheduler

    # unit must be: minutes, hours, days or weeks
    kwargs = {unit: quantity}

    job_id = str(uuid.uuid4())[:8]

    error_message = ast.literal_eval(error_message)

    if error_message:
        scheduler.add_job(check_messages, 'interval', [job_id, company_id, quantity, unit, callback, status_code], id=job_id, **kwargs, name=company_id)
    else:
        scheduler.add_job(check, 'interval', [job_id, company_id, quantity, unit, callback, status_code], id=job_id, **kwargs, name=company_id)

    callback("[job_id: *{}*] Watching company *{}*!".format(job_id, company_id))
    callback("Use `@logentries_bot remove --job_id \"{}\"` to stop monitoring company *{}*".format(job_id, company_id))


def remove_company(job_id, callback):
    global scheduler

    job = scheduler.get_job(job_id=job_id)
    if job:
        company_id = str(job.name)

    try:
        scheduler.pause_job(job_id=job_id)
        scheduler.remove_job(job_id=job_id)
    except:
        callback("Error! Check job_id and try again!")

    callback("[job_id: *{}*] Stopped monitoring company *{}*!".format(job_id, company_id))


def get_how_many(company_id, from_time, status_code=400):
    statement = "where(statusCode={status_code} \
    AND _id={id} \
    AND /POST/) \
    groupby(_id) \
    calculate(count)".format(status_code=status_code, id=company_id)

    to_time = Time.get_timestamp(
        datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    )

    logs = (
        LogentriesHelper.get_all_test_environment() +
        LogentriesHelper.get_all_live_environment()
    )

    query = Query(statement, {
            'from': from_time, 'to': to_time
        }, logs)

    response = LogentriesConnection(
        config('LOGENTRIES_API_KEY')
    ).post("/query/logs", query.build())

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
    statement = "where(statusCode={status_code} \
     AND _id={id} \
     AND /POST/)".format(status_code=status_code, id=company_id)

    to_time = Time.get_timestamp(
        datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    )

    logs = (
        LogentriesHelper.get_all_test_environment() +
        LogentriesHelper.get_all_live_environment()
    )

    query = Query(statement, {
        'from': from_time,
        'to': to_time
    }, logs)

    client = LogentriesConnection(config('LOGENTRIES_API_KEY'))
    response = client.post("/query/logs", query.build())

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


def get_jobs(callback):
    global scheduler

    jobs = scheduler.get_jobs()

    callback("Running jobs: ")
    for job in jobs:
        callback("job_id: *{}* watching company *{}*".format(job.id, job.name))
