from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.boolean import WBoolean


class HasCharsTest(TestCase):

    def test_has_chars_on_empty_stream_returns_false(self):
        # when
        result = eval_str("(has_chars (stream \"\"))", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)

    def test_has_chars_on_non_empty_stream_returns_true(self):
        # when
        result = eval_str("(has_chars (stream \"abc\"))",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)
