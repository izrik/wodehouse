import unittest

from functions.collections import w_to_list
from functions.str import w_str
from wtypes.control import WRaisedException
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.set import WSet


class ToListTest(unittest.TestCase):
    def test_set_yield_list(self):
        # given
        s = WSet(WNumber(1), WNumber(2), WNumber(3))
        # precondition
        self.assertEqual(len(s), 3)
        self.assertIn(1, s)
        self.assertIn(2, s)
        self.assertIn(3, s)
        # when
        result = w_to_list(s)
        # then
        self.assertEqual(len(result), 3)
        # order is not guaranteed coming from a set
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)

    def test_list_yield_different_list(self):
        # given
        s = WList(WNumber(1), WNumber(2), WNumber(3))
        # precondition
        self.assertEqual(s, [1, 2, 3])
        # when
        result = w_to_list(s)
        # then
        self.assertEqual(result, [1, 2, 3])
        # and it's not the same list object
        self.assertIsNot(result, s)

    def test_non_wobject_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_to_list(1)
        # and
        self.assertEqual(str(exc.exception),
                         'Argument "s" to w_to_list must be a WObject. '
                         'Got "1" (<class \'int\'>) instead.')

    def test_non_wcollection_wraises(self):
        # when
        result = w_to_list(WNumber(1))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message),
                         'Argument "s" to to_list must be a list or set. '
                         'Got "1" (Number) instead.')
