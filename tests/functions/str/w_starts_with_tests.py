from unittest import TestCase

from functions.eval import eval_str
from functions.str import w_starts_with
from modules.builtins import create_builtins_module
from wtypes.boolean import WBoolean
from wtypes.string import WString


class StartsWithTest(TestCase):

    def test_empty_string_starts_with_empty_string(self):
        # when
        result = w_starts_with(WString(""), WString(""))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(starts_with \"\" \"\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_starts_with_itself(self):
        # when
        result = w_starts_with(WString("abcd"), WString("abcd"))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(starts_with \"abcd\" \"abcd\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_starts_with_empty_string(self):
        # when
        result = w_starts_with(WString("abcd"), WString(""))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(starts_with \"abcd\" \"\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_starts_with_prefix(self):
        # when
        result = w_starts_with(WString("abcd"), WString("ab"))
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(starts_with \"abcd\" \"ab\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_string_does_not_start_with_non_prefix(self):
        # when
        result = w_starts_with(WString("abcd"), WString("efg"))
        # then
        self.assertIs(WBoolean.false, result)
        # when
        result = eval_str("(starts_with \"abcd\" \"efg\")",
                          create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)
