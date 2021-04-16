import unittest

from functions.collections import w_add
from wtypes.control import WRaisedException
from wtypes.number import WNumber
from wtypes.set import WSet


class SetAddTests(unittest.TestCase):
    def test_add_adds_value(self):
        # given
        s = WSet(WNumber(123))
        # precondition
        self.assertEqual(len(s), 1)
        self.assertIn(WNumber(123), s)
        self.assertNotIn(WNumber(456), s)
        # when
        result = w_add(s, WNumber(456))
        # then
        self.assertEqual(len(s), 2)
        self.assertIn(WNumber(123), s)
        self.assertIn(WNumber(456), s)
        # and
        self.assertIs(result, s)

    def test_non_wobject_raises_1(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_add(123, WNumber(456))
        # and
        self.assertEqual(str(exc.exception),
                         f'Arguments to add must be WObject. Got "123" '
                         f'(<class \'int\'>) instead.')

    def test_non_wset_wraises(self):
        # when
        result = w_add(WNumber(123), WNumber(456))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message,
                         'Argument "s" must be a set. '
                         'Got "123" (Number) instead.')

    def test_non_wobject_raises_2(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_add(WSet(WNumber(123)), 456)
        # and
        self.assertEqual(str(exc.exception),
                         f'Arguments to add must be WObject. Got "456" '
                         f'(<class \'int\'>) instead.')

    def test_unhashable_type_wraises(self):
        # given
        s1 = WSet()
        s2 = WSet()
        # when
        result = w_add(s1, s2)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(result.exception.message, 'Unhashable type: "Set"')
