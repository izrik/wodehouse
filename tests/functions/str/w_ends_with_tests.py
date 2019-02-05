from unittest import TestCase

from functions.eval import eval_str
from functions.str import w_ends_with
from modules.builtins import create_builtins_module
from wtypes.boolean import WBoolean
from wtypes.string import WString


class EndsWithTest(TestCase):

    def test_empty_string_ends_with_empty_string(self):
        # when
        result = w_ends_with(WString(""), WString(""))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(ends_with \"\" \"\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_ends_with_itself(self):
        # when
        result = w_ends_with(WString("abcd"), WString("abcd"))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(ends_with \"abcd\" \"abcd\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_ends_with_empty_string(self):
        # when
        result = w_ends_with(WString("abcd"), WString(""))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(ends_with \"abcd\" \"\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_ends_with_suffix(self):
        # when
        result = w_ends_with(WString("abcd"), WString("cd"))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(ends_with \"abcd\" \"cd\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_does_not_end_with_non_suffix(self):
        # when
        result = w_ends_with(WString("abcd"), WString("efg"))
        # then
        self.assertIs(WBoolean.false, result)
        # when
        result = eval_str("(ends_with \"abcd\" \"efg\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)
