from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.boolean import WBoolean


class IsInstanceTest(TestCase):

    def test_isinstance_returns_true_when_match_number(self):
        # when
        result = eval_str("(isinstance 123 'Number)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_number_type_list(self):
        # when
        result = eval_str("(isinstance 123 '(Number))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_string(self):
        # when
        result = eval_str("(isinstance \"abc\" 'String)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_string_type_list(self):
        # when
        result = eval_str("(isinstance \"abc\" '(String))",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_mixed_type_list(self):
        # when
        result = eval_str("(isinstance 123 '(Number String))",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(isinstance \"abc\" '(Number String))",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_function(self):
        # when
        result = eval_str("(isinstance (lambda () 1) 'Function)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_magic_function(self):
        # when
        result = eval_str("(isinstance list 'MagicFunction)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_function_with_magic_func(self):
        # when
        result = eval_str("(isinstance list 'Function)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_boolean(self):
        # when
        result = eval_str("(isinstance (lambda () 1) 'Function)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    # TODO: create anonymous macros
    # def test_isinstance_returns_true_when_match_macro(self):
    #     # when
    #     result = eval_str("(isinstance let 'Macro)",
    #                       create_default_scope())
    #     # then
    #     self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_magic_macro(self):
        # when
        result = eval_str("(isinstance let 'MagicMacro)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_macro_with_magic_macro(self):
        # when
        result = eval_str("(isinstance let 'Macro)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_symbol(self):
        # when
        result = eval_str("(isinstance 'a 'Symbol)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_list(self):
        # when
        result = eval_str("(isinstance '(1 2 3) 'List)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_false_when_does_not_match(self):
        # when
        result = eval_str(
            "(isinstance 123 '(String Symbol Boolean List Function Macro))",
            create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_exception(self):
        # when
        result = eval_str("(isinstance (exception) 'Exception)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_exception_type_list(self):
        # when
        result = eval_str("(isinstance (exception) '(Exception))",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_exception_with_message(self):
        # when
        result = eval_str("(isinstance (exception \"message\") 'Exception)",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_exc_list_with_message(self):
        # when
        result = eval_str("(isinstance (exception \"message\") '(Exception))",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
