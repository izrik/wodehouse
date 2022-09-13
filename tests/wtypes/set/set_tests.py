import unittest

from functions.str import w_str
from wtypes.list import WList
from wtypes.set import WSet
from wtypes.number import WNumber
from wtypes.string import WString


class SetTests(unittest.TestCase):
    def test_create(self):
        # when
        result = WSet()
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WSet)
        self.assertEqual(len(result), 0)

    def test_create_with_value(self):
        # when
        result = WSet(WNumber(123))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WSet)
        self.assertEqual(len(result), 1)
        self.assertTrue(WNumber(123) in result)
        self.assertIn(WNumber(123), result)

    def test_create_with_values(self):
        # when
        result = WSet(WNumber(123), WNumber(456))
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WSet)
        self.assertEqual(len(result), 2)
        self.assertIn(WNumber(123), result)
        self.assertIn(WNumber(456), result)

    def test_add_adds_a_value(self):
        # given
        s = WSet(WNumber(123))
        # precondition
        self.assertEqual(len(s), 1)
        self.assertIn(WNumber(123), s)
        self.assertNotIn(WNumber(456), s)
        # when
        result = s.add(WNumber(456))
        # then
        self.assertEqual(len(s), 2)
        self.assertIn(WNumber(123), s)
        self.assertIn(WNumber(456), s)
        # and
        self.assertIs(result, s)

    def test_iterate(self):
        # given
        s = WSet(WNumber(123), WNumber(456))
        # precondition
        self.assertEqual(len(s), 2)
        self.assertIn(WNumber(123), s)
        self.assertIn(WNumber(456), s)
        # when
        lst = WList(*s)
        # then
        self.assertEqual(len(lst), 2)
        self.assertIn(WNumber(123), lst)
        self.assertIn(WNumber(456), lst)
        self.assertTrue(lst == [WNumber(123), WNumber(456)] or
                        lst == [WNumber(456), WNumber(123)])

    def test_equality(self):
        # given
        s1 = WSet(WNumber(123))
        s2 = WSet(WNumber(123))
        # expect
        self.assertTrue(s1 == s2)
        self.assertEqual(s1, s2)
        # and
        self.assertEqual(s1, {123})

    def test_inequality(self):
        # given
        s1 = WSet(WNumber(123))
        s2 = WSet(WNumber(456))
        # expect
        self.assertTrue(s1 != s2)
        self.assertNotEqual(s1, s2)
        # and
        self.assertNotEqual(s1, {456})

    def test_equality_with_wrong_type(self):
        # given
        s = WSet(WNumber(123))
        # expect
        self.assertNotEqual(s, "string")

    def test_repr(self):
        # given
        s = WSet(WNumber(123))
        # when
        result = s.__repr__()
        # then
        self.assertIsInstance(result, str)
        self.assertEqual(result, "WSet(WNumber(123))")

    def test_str(self):
        # given
        s = WSet(WNumber(123))
        # when
        result = s.__str__()
        # then
        self.assertIsInstance(result, str)
        self.assertEqual(result, "(set 123)")

    def test_w_str(self):
        # given
        s = WSet(WNumber(123))
        # when
        result = w_str(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, "(set 123)")
