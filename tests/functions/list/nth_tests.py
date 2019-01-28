from unittest import TestCase

from functions.list import nth
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.number import WNumber


class NthTest(TestCase):
    def test_zero_returns_first_item(self):
        # given
        x = WList(WNumber(1), WNumber(2), WNumber(3))
        # when
        result = nth(x, WNumber(0))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_one_returns_second_item(self):
        # given
        x = WList(WNumber(1), WNumber(2), WNumber(3))
        # when
        result = nth(x, WNumber(1))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WNumber)
        self.assertEqual(2, result)

    def test_negative_one_returns_last_item(self):
        # given
        x = WList(WNumber(1), WNumber(2), WNumber(3))
        # when
        result = nth(x, WNumber(-1))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WNumber)
        self.assertEqual(3, result)

    def test_negative_two_returns_second_to_last_item(self):
        # given
        x = WList(WNumber(1), WNumber(2), WNumber(3))
        # when
        result = nth(x, WNumber(-2))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WNumber)
        self.assertEqual(2, result)

    def test_index_too_high_raises_exception(self):
        # given
        x = WList(WNumber(1), WNumber(2), WNumber(3))
        # when
        result = nth(x, WNumber(3))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("IndexError: index out of bounds",
                         result.exception.message)

    def test_negative_index_to_low_raises_exception(self):
        # given
        x = WList(WNumber(1), WNumber(2), WNumber(3))
        # when
        result = nth(x, WNumber(-4))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("IndexError: index out of bounds",
                         result.exception.message)

    # TODO: slices, etc
    # TODO argument types
