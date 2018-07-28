from datetime import datetime, timezone


def do(*handlers):
    def invoke_all():
        for handler in handlers:
            handler()
    return invoke_all


def turn_lamp_off(lamp):
    return lambda: lamp.off()


def turn_lamp_on(lamp):
    return lambda: lamp.on()


def when(filter, handler):
    def wrapper(value):
        if filter(value):
            handler()
    return wrapper


def with_current_time(*handlers):
    def invoke():
        now = datetime.now(timezone.utc)
        for handler in handlers:
            handler(now)
    return invoke
