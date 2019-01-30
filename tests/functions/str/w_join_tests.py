from unittest import TestCase

from functions.eval import eval_str
from functions.str import w_join
from modules.builtins import create_builtins_module
from wtypes.list import WList
from wtypes.string import WString


class JoinTest(TestCase):

    def test_joins_strings_with_delimiter(self):
        # when
        result = w_join(WString("-"), WList(WString("a"),
                                            WString("b"),
                                            WString("c")))
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a-b-c", result)
        # when
        result = eval_str("(join \"-\" '(\"a\" \"b\" \"c\"))",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a-b-c", result)

    def test_empty_string_concatenates(self):
        # when
        result = w_join(WString(""), WList(WString("a"),
                                           WString("b"),
                                           WString("c")))
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("abc", result)
        # when
        result = eval_str("(join \"\" '(\"a\" \"b\" \"c\"))",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("abc", result)

    def test_empty_list_yields_empty_string(self):
        # when
        result = w_join(WString("delim"), WList())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("", result)
        # when
        result = eval_str("(join \"delim\" '())",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("", result)
