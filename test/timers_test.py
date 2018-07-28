from astral import Astral
from datetime import datetime, time, timedelta, timezone
from freezegun import freeze_time
from talons import timers
from unittest import TestCase
from unittest.mock import MagicMock, patch

LOCATION = "Raleigh"


class TimersTest(TestCase):

    @freeze_time()
    @patch('threading.Timer')
    def test_after(self, Timer):
        delta = timedelta(seconds=10)

        def handler(): None

        timers.after(delta, handler)
        Timer.assert_called_once_with(delta.total_seconds(), handler)
        Timer.return_value.start.assert_called_once_with()

    @freeze_time()
    @patch('threading.Timer')
    def test_at(self, Timer):
        delta = timedelta(seconds=10)
        now = datetime.now(timezone.utc)

        def handler(): None

        timers.at(now + delta, handler)
        Timer.assert_called_once_with(delta.total_seconds(), handler)
        Timer.return_value.start.assert_called_once_with()

    @freeze_time("2018-07-19 19:30:00")
    def test_next_before_default(self):
        next = timers.next(time(20, 0, 0, tzinfo=timezone.utc))
        expected = datetime(
            2018, 7, 20, 20, 0, 0,
            tzinfo=timezone.utc
        )
        self.assertEqual(next, expected)

    @freeze_time("2018-07-19 19:30:00")
    def test_next_before_minimum(self):
        minimum = timedelta(minutes=5)
        next = timers.next(
            time(20, 0, 0, tzinfo=timezone.utc),
            minimum=minimum
        )
        expected = datetime(
            2018, 7, 19, 20, 0, 0,
            tzinfo=timezone.utc
        )
        self.assertEqual(next, expected)

    @freeze_time("2018-07-19 20:30:00")
    def test_next_after(self):
        next = timers.next(time(20, 0, 0, tzinfo=timezone.utc))
        expected = datetime(
            2018, 7, 20, 20, 0, 0,
            tzinfo=timezone.utc
        )
        self.assertEqual(next, expected)

    def test_local_timezone(self):
        delta = datetime.now() - datetime.utcnow()
        minutes = round(delta.total_seconds() / 60)
        expected = timezone(timedelta(minutes=minutes))
        self.assertEqual(timers.local_timezone(), expected)

    @freeze_time()
    @patch("talons.timers.at")
    @patch("talons.timers.next")
    def test_at_dawn(self, next, at):
        handler = MagicMock()
        location = Astral()[LOCATION]
        timers.at_dawn(handler)
        next.assert_called_once_with(location.dawn(local=False).timetz())
        at.assert_called_once_with(next.return_value, handler)
        handler.assert_not_called()

    @freeze_time()
    @patch("talons.timers.at")
    @patch("talons.timers.next")
    def test_at_dusk(self, next, at):
        handler = MagicMock()
        location = Astral()[LOCATION]
        timers.at_dusk(handler)
        next.assert_called_once_with(location.dusk(local=False).timetz())
        at.assert_called_once_with(next.return_value, handler)
        handler.assert_not_called()

    @freeze_time()
    @patch("talons.timers.at")
    @patch("talons.timers.fuzz")
    @patch("talons.timers.next")
    def test_at_morning(self, next, fuzz, at):
        handler = MagicMock()
        timers.at_morning(handler)
        next.assert_called_once_with(timers.MORNING)
        fuzz.assert_called_once_with(next.return_value, timers.DEFAULT_FUZZ)
        at.assert_called_once_with(fuzz.return_value, handler)
        handler.assert_not_called()

    @freeze_time()
    @patch("talons.timers.at")
    @patch("talons.timers.fuzz")
    @patch("talons.timers.next")
    def test_at_night(self, next, fuzz, at):
        handler = MagicMock()
        timers.at_night(handler)
        next.assert_called_once_with(timers.NIGHT)
        fuzz.assert_called_once_with(next.return_value, timers.DEFAULT_FUZZ)
        at.assert_called_once_with(fuzz.return_value, handler)
        handler.assert_not_called()

    def test_fuzz(self):
        fuzz = timedelta(minutes=15)
        origin = datetime.now(timezone.utc)
        fuzzed = timers.fuzz(origin, fuzz)
        self.assertNotEqual(origin, fuzzed)
        self.assertGreaterEqual(fuzzed, origin - fuzz)
        self.assertLessEqual(fuzzed, origin + fuzz)

    def test_always(self):
        condition = MagicMock()
        handler = MagicMock()
        timers.always(condition, handler)
        self.assertEqual(condition.call_count, 1)
        ((wrapper,), _) = condition.call_args
        self.assertTrue(callable(wrapper))
        handler.assert_not_called()
        wrapper()
        handler.assert_called_once_with()
        self.assertEqual(condition.call_count, 2)
        ((wrapper,), _) = condition.call_args
        self.assertTrue(callable(wrapper))
