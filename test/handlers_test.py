from datetime import datetime, timezone
from freezegun import freeze_time
from talons import handlers
from unittest import TestCase
from unittest.mock import MagicMock


class HandlersTest(TestCase):

    def test_turn_lamp_off(self):
        lamp = MagicMock()
        handler = handlers.turn_lamp_off(lamp)
        lamp.off.assert_not_called()
        handler()
        lamp.off.assert_called_once_with()

    def test_turn_lamp_on(self):
        lamp = MagicMock()
        handler = handlers.turn_lamp_on(lamp)
        lamp.on.assert_not_called()
        handler()
        lamp.on.assert_called_once_with()

    @freeze_time()
    def test_with_current_time(self):
        now = datetime.now(timezone.utc)
        handler_one = MagicMock()
        handler_two = MagicMock()

        wrapper = handlers.with_current_time(handler_one, handler_two)
        wrapper()

        handler_one.assert_called_once_with(now)
        handler_two.assert_called_once_with(now)

    def test_when(self):
        handler = MagicMock()

        def filter(value):
            return value

        when = handlers.when(filter, handler)

        handler.assert_not_called()
        when(False)
        handler.assert_not_called()
        when(True)
        handler.assert_called_once_with()

    def test_do(self):
        handler1 = MagicMock()
        handler2 = MagicMock()
        wrapper = handlers.do(handler1, handler2)
        handler1.assert_not_called()
        handler2.assert_not_called()
        wrapper()
        handler1.assert_called_once_with()
        handler2.assert_called_once_with()
