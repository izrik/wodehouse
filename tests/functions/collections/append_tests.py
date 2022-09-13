import unittest

# import pytest as pytest

from functions.collections import w_append
from wtypes.control import WRaisedException
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.set import WSet
from wtypes.string import WString


class AppendTests(unittest.TestCase):
    def test_empty_list_append_adds_to_the_list(self):
        # given
        lst = WList()
        # precondition
        self.assertEqual(len(lst), 0)
        # when
        result = w_append(lst, WNumber(123))
        # then
        self.assertIs(result, lst)  # does not create new object
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], WNumber(123))

    def test_non_empty_list_append_adds_to_end_of_list(self):
        # given
        lst = WList(WNumber(1), WNumber(2), WNumber(3))
        # precondition
        self.assertEqual(len(lst), 3)
        self.assertEqual(lst[0], WNumber(1))
        self.assertEqual(lst[1], WNumber(2))
        self.assertEqual(lst[2], WNumber(3))
        # when
        result = w_append(lst, WNumber(4))
        # then
        self.assertIs(result, result)  # does not create new object
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], WNumber(1))
        self.assertEqual(result[1], WNumber(2))
        self.assertEqual(result[2], WNumber(3))
        self.assertEqual(result[3], WNumber(4))

    def test_set_instead_of_list_wraises(self):
        # given
        s = WSet()
        # when
        result = w_append(s, WNumber(123))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message, WString(
            'Argument "lst" must be a List. Got "(set )" (Set) instead.'))

    def test_non_wobject_instead_of_list_raises(self):
        # given
        s = set()
        # expect
        with self.assertRaises(TypeError) as exc:
            w_append(s, WNumber(123))
        # and
        self.assertEqual(str(exc.exception),
                         'Arguments to w_append must be WObject. Got "set()" '
                         '(<class \'set\'>) instead.')
