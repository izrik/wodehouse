import unittest

from wtypes.control import WRaisedException
from wtypes.number import WNumber
from wtypes.string import WString


class ConcatenationTest(unittest.TestCase):
    def test_add_wstrings_concatenates_them(self):
        # when
        result = WString("a") + WString("b")
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, "ab")

    def test_non_wobject_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            WString("a") + "b"
        # and
        self.assertEqual(str(exc.exception),
                         'Operand must be a WObject. '
                         'Got b (<class \'str\'>) instead.')

    def test_non_wstring_wraises(self):
        # when
        result = WString("a") + WNumber(3)
        # and
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         'Unsupported operand type(s) for +: '
                         '"String" and "Number"')
