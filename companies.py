import json
from datetime import datetime as dt
from datetime import timedelta
from query import get_timestamp, post_query


def get_companies_with_error_400(from_time):
    statement = "where(statusCode=400) groupby(_id) calculate(count)"
    to_time = get_timestamp(dt.strftime(dt.now(), "%d/%m/%Y %H:%M:%S"))

    response = post_query(statement, from_time, to_time)
    response = json.loads(response)

    companies = []
    for i in range(0, len(response['statistics']['groups'])):
        for key in response['statistics']['groups'][i].keys():
            companies.append(key)

    return companies


def get_interval_bound(quantity, unit):
    # unit must be: minutes, hours, days or weeks
    kwargs = {unit: quantity}

    to_time = dt.now()
    from_time = to_time - timedelta(**kwargs)

    from_time = dt.strftime(from_time, "%d/%m/%Y %H:%M:%S")
    from_time = get_timestamp(from_time)

    return from_time


def add_company(company_id, interval, request_method, error_codes):
    pass


if __name__ == '__main__':
    f = get_interval_bound(1, 'weeks')
    companies = get_companies_with_error_400(f)
    print(companies)
