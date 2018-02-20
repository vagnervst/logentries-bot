from logentriesbot.client.logentries import get_interval_bound, get_how_many_400


def check(company_id, quantity, unit):
    from_time = get_interval_bound(quantity, unit)
    return "Company {} had {} errors in last {} {}!".format(company_id, get_how_many_400(company_id, from_time), str(quantity), unit)
