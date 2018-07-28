from astral import Astral

astral = Astral()
location = astral["Raleigh"]


def after_time(start):
    return lambda datetime: datetime.time() > start


def all_of(*filters):
    return lambda value: all(map(lambda filter: filter(value), filters))


def before_time(end):
    return lambda datetime: datetime.time() < end


def night(datetime):
    date = datetime.date()
    (dawn, dusk) = location.daylight(date=date, local=False)
    return datetime < dawn or datetime > dusk


def some_of(*filters):
    return lambda value: any(map(lambda filter: filter(value), filters))
