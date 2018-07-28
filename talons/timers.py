from astral import Astral
from datetime import datetime, time, timedelta, timezone
from random import randint

import threading


def after(delay, handler):
    threading.Timer(delay.total_seconds(), handler).start()


def always(when, handler):
    def wrapper():
        handler()
        when(wrapper)
    when(wrapper)


def at(when, handler):
    now = datetime.now(timezone.utc)
    delay = when - now
    after(delay, handler)


def at_dawn(handler):
    location = Astral()[LOCATION]
    dawn = next(location.dawn(local=False).timetz())
    return at(dawn, handler)


def at_dusk(handler):
    location = Astral()[LOCATION]
    dusk = next(location.dusk(local=False).timetz())
    return at(dusk, handler)


def at_morning(handler):
    morning = fuzz(next(MORNING), DEFAULT_FUZZ)
    return at(morning, handler)


def at_night(handler):
    night = fuzz(next(NIGHT), DEFAULT_FUZZ)
    return at(night, handler)


def fuzz(origin, fuzz):
    seconds = fuzz.total_seconds()
    delta = timedelta(seconds=randint(-seconds, seconds))
    return origin + delta


def local_timezone():
    delta = datetime.now() - datetime.utcnow()
    minutes = round(delta.total_seconds() / 60)
    return timezone(timedelta(minutes=minutes))


def next(time, minimum=timedelta(hours=1)):
    now = datetime.now(timezone.utc)
    if (now + minimum).timetz() < time:
        return datetime.combine(now.date(), time)
    else:
        return datetime.combine(now.date() + timedelta(days=1), time)


DEFAULT_FUZZ = timedelta(minutes=10)
LOCATION = "Raleigh"
MORNING = time(5, 10, 0, tzinfo=local_timezone())
NIGHT = time(22, 30, 0, tzinfo=local_timezone())
