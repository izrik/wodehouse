import unittest

from functions.str import w_replace
from wtypes.control import WRaisedException
from wtypes.number import WNumber
from wtypes.string import WString


class ReplaceTest(unittest.TestCase):
    def test_simple_string(self):
        # when
        result = w_replace(WString("abcdefg"), WString("cde"), WString("123"))
        # then
        self.assertEqual(result, "ab123fg")

    def test_none_s_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_replace(None, WString("cde"), WString("123"))
        # and
        self.assertEqual(
            str(exc.exception),
            'Argument "s" to replace should be a WString. Got "None" '
            '(<class \'NoneType\'>) instead.')

    def test_int_s_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_replace(1, WString("cde"), WString("123"))
        # and
        self.assertEqual(
            str(exc.exception),
            'Argument "s" to replace should be a WString. Got "1" '
            "(<class 'int'>) instead.")

    def test_non_wstring_s_wraises(self):
        # when
        result = w_replace(WNumber(123), WString("123"), WString("abc"))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         'Argument "s" to replace should be a String. '
                         'Got "123" (Number) instead.')

    def test_none_old_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_replace(WString("cde"), None, WString("123"))
        # and
        self.assertEqual(
            str(exc.exception),
            'Argument "old" to replace should be a WString. Got "None" '
            '(<class \'NoneType\'>) instead.')

    def test_int_old_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_replace(WString("cde"), 1, WString("123"))
        # and
        self.assertEqual(
            str(exc.exception),
            'Argument "old" to replace should be a WString. Got "1" '
            "(<class 'int'>) instead.")

    def test_non_wstring_old_wraises(self):
        # when
        result = w_replace(WString("123"), WNumber(123), WString("abc"))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         'Argument "old" to replace should be a String. '
                         'Got "123" (Number) instead.')

    def test_none_new_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_replace(WString("cde"), WString("123"), None)
        # and
        self.assertEqual(
            str(exc.exception),
            'Argument "new" to replace should be a WString. Got "None" '
            '(<class \'NoneType\'>) instead.')

    def test_int_new_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_replace(WString("cde"), WString("123"), 1)
        # and
        self.assertEqual(
            str(exc.exception),
            'Argument "new" to replace should be a WString. Got "1" '
            "(<class 'int'>) instead.")

    def test_non_wstring_new_wraises(self):
        # when
        result = w_replace(WString("123"), WString("abc"), WNumber(123))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         'Argument "new" to replace should be a String. '
                         'Got "123" (Number) instead.')

    def test_all_instances_are_replaced(self):
        # when
        result = w_replace(WString("axbxcxd"), WString("x"), WString("yz"))
        # then
        self.assertEqual(result, "ayzbyzcyzd")

    def test_old_not_found_returns_s_unchanged(self):
        # when
        result = w_replace(WString("abcdefg"), WString("x"), WString("yz"))
        # then
        self.assertEqual(result, "abcdefg")
