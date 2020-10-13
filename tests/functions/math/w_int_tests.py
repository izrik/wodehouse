import unittest

from functions.math import w_int
from wtypes.control import WRaisedException
from wtypes.number import WNumber


class WIntTest(unittest.TestCase):
    def test_int_yields_same(self):
        # when
        result = w_int(WNumber(123))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 123)

    def test_float_yields_truncated(self):
        # when
        result = w_int(WNumber(123.45))
        # then
        self.assertEqual(result, 123)

    def test_negative_int_yields_same(self):
        # when
        result = w_int(WNumber(1123))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 1123)

    def test_negative_float_yields_truncated(self):
        # when
        result = w_int(WNumber(-123.45))
        # then
        self.assertEqual(result, -123)

    def test_non_wobject_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_int(123)
        # and
        self.assertEqual(str(exc.exception),
                         'Argument to w_int should be a WObject. '
                         'Got "123" (<class \'int\'>) instead.')

    def test_non_wnumber_wraises(self):
        # when
        from wtypes.list import WList
        result = w_int(WList())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         'Argument to int should be a Number. '
                         'Got "()" (List) instead.')

    # TODO: WString inputs?
