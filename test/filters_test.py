from datetime import datetime, timezone
from talons import filters
from unittest import TestCase


class FiltersTest(TestCase):

    def test_after_time(self):
        midnight = datetime(2018, 7, 15, 0, 0, 0, tzinfo=timezone.utc)
        morning = datetime(2018, 7, 15, 6, 0, 0, tzinfo=timezone.utc)
        noon = datetime(2018, 7, 15, 12, 0, 0, tzinfo=timezone.utc)

        after = filters.after_time(morning.time())
        self.assertTrue(after(noon))
        self.assertFalse(after(midnight))

    def test_before_time(self):
        midnight = datetime(2018, 7, 15, 0, 0, 0, tzinfo=timezone.utc)
        morning = datetime(2018, 7, 15, 6, 0, 0, tzinfo=timezone.utc)
        noon = datetime(2018, 7, 15, 12, 0, 0, tzinfo=timezone.utc)

        before = filters.before_time(morning.time())
        self.assertTrue(before(midnight))
        self.assertFalse(before(noon))

    def test_night(self):
        midnight = datetime(2018, 7, 15, 0, 0, 0, tzinfo=timezone.utc)
        noon = datetime(2018, 7, 15, 12, 0, 0, tzinfo=timezone.utc)
        self.assertTrue(filters.night(midnight))
        self.assertFalse(filters.night(noon))

    def test_some_of(self):
        def false(value):
            return False

        def true(value):
            return True

        false_false = filters.some_of(false, false)
        false_true = filters.some_of(false, true)
        true_false = filters.some_of(true, false)
        true_true = filters.some_of(true, true)

        self.assertFalse(false_false(None))
        self.assertTrue(false_true(None))
        self.assertTrue(true_false(None))
        self.assertTrue(true_true(None))

    def test_all_of(self):
        def false(value):
            return False

        def true(value):
            return True

        false_false = filters.all_of(false, false)
        false_true = filters.all_of(false, true)
        true_false = filters.all_of(true, false)
        true_true = filters.all_of(true, true)

        self.assertFalse(false_false(None))
        self.assertFalse(false_true(None))
        self.assertFalse(true_false(None))
        self.assertTrue(true_true(None))
