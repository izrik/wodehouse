from unittest import TestCase

from functions.eval import eval_str
from functions.str import w_format
from modules.builtins import create_builtins_module
from wtypes.string import WString


class FormatTest(TestCase):

    def test_format_interpolates_arguments(self):
        # when
        result = eval_str("(format \"one {} three\" \"two\")",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("one two three", result)

    def test_format_interprets_double_braces_as_escaped(self):
        # when
        result = eval_str("(format \"abc {{ def\")", create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("abc { def", result)

    def test_format_stringifies_arguments(self):
        # when
        result = eval_str("(format \"a{}b{}c{}d\" 1 true +)",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a1btruec+d", result)

    def test_format_leading_braces_interpolated_with_nothing_before(self):
        # when
        result = w_format(WString("{} something"), WString("say"))
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("say something", result)
        # when
        result = eval_str("(format \"{} something\" \"say\")",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("say something", result)

    def test_format_trailing_braces_interpolated_with_nothing_after(self):
        # when
        result = w_format(WString("say {}"), WString("something"))
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("say something", result)
        # when
        result = eval_str("(format \"say {}\" \"something\")",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("say something", result)