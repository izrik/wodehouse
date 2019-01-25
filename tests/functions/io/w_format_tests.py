from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.string import WString


class FormatTest(TestCase):

    def test_format_interpolates_arguments(self):
        # when
        result = eval_str("(format \"one {} three\" \"two\")",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("one two three", result)

    def test_format_interprets_double_braces_as_escaped(self):
        # when
        result = eval_str("(format \"abc {{ def\")", create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("abc { def", result)

    def test_format_stringifies_arguments(self):
        # when
        result = eval_str("(format \"a{}b{}c{}d\" 1 true +)",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a1btruec+d", result)