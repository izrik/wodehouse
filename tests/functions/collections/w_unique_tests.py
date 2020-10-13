import unittest

from functions.collections import w_unique
from wtypes.control import WRaisedException
from wtypes.list import WList
from wtypes.number import WNumber


class WUniqueTest(unittest.TestCase):
    def test_unique(self):
        # given
        x = WList(1, 2, 3, 3)
        # when
        result = w_unique(x)
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual(3, len(result))
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)

    def test_unique_non_wobject_raisees(self):
        # given
        x = [1, 2, 3, 3]
        # expect
        with self.assertRaises(TypeError) as exc:
            w_unique(x)
        # and
        msg = str(exc.exception)
        self.assertEqual(msg,
                         f'Argument to unique must be a WObject. Got "{x}" '
                         f'(<class \'list\'>) instead.')

    def test_unique_non_wlist_wraisees(self):
        # given
        x = WNumber(2)
        # when
        result = w_unique(x)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         f'Argument to unique must be a '
                         f'list. Got "2" (Number) instead.')
