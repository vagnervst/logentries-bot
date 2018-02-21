from apscheduler.schedulers.background import BackgroundScheduler
from logentriesbot.client.logentries import get_interval_bound, get_how_many_400


def check(company_id, quantity, unit):
    from_time = get_interval_bound(quantity, unit)
    print("Company {} had {} errors in last {} {}!".format(company_id, get_how_many_400(company_id, from_time), str(quantity), unit))
    return "Company {} had {} errors in last {} {}!".format(company_id, get_how_many_400(company_id, from_time), str(quantity), unit)


def add_company(company_id, quantity, unit):
    # unit must be: minutes, hours, days or weeks
    kwargs = {unit: quantity}

    scheduler = BackgroundScheduler()
    scheduler.add_job(check, 'interval', [company_id, quantity, unit], **kwargs)
    scheduler.start()

    return "Watching company {}".format(company_id)
