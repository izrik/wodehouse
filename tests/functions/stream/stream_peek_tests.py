from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.stream import WStream
from wtypes.string import WString


class PeekTest(TestCase):

    def test_peek_returns_next_char(self):
        # when
        result = eval_str("(peek (stream \"abc\"))", create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a", result)

    def test_peek_does_not_advance_position(self):
        # given
        s = WStream("abc")
        scope = create_builtins_module()
        scope['s'] = s
        # precondition
        self.assertEqual(eval_str("(peek s)", scope), "a")
        # expect
        self.assertEqual(eval_str("(peek s)", scope), "a")
        self.assertEqual(eval_str("(peek s)", scope), "a")
