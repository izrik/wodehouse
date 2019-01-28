from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.string import WString


class StringTest(TestCase):

    def test_str_stringifies_numbers(self):
        # when
        result = eval_str("(str 123)", create_builtins_module())
        # then
        self.assertEqual("123", result)

    def test_str_strings_are_unchanged(self):
        # when
        result = eval_str("(str \"123\")", create_builtins_module())
        # then
        self.assertEqual("123", result)

    def test_str_stringifies_lists(self):
        # when
        result = eval_str("(str (list 1 2 3))", create_builtins_module())
        # then
        self.assertEqual("(1 2 3)", result)

    def test_str_stringifies_quoted_lists(self):
        # when
        result = eval_str("(str '(1 2 3))", create_builtins_module())
        # then
        self.assertEqual("(1 2 3)", result)

    def test_str_stringifies_symbols(self):
        # when
        result = eval_str("(str 'asdf)", create_builtins_module())
        # then
        self.assertEqual("asdf", result)

    def test_str_stringifies_quoted_symbols(self):
        # when
        result = eval_str("(str ''asdf)", create_builtins_module())
        # then
        self.assertEqual("'asdf", result)

    def test_str_stringifies_lambdas(self):
        # when
        result = eval_str("(str (lambda (x) (* x x)))",
                          create_builtins_module())
        # then
        self.assertEqual("(lambda (x) (* x x))", result)

    def test_str_stringifies_magic_functions(self):
        # when
        result = eval_str("(str str)", create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertTrue(result.value.startswith("str"))

    def test_str_stringifies_variables_values(self):
        # when
        result = eval_str("(let (a 123) (str a))", create_builtins_module())
        # then
        self.assertEqual("123", result)

    def test_str_stringifies_boolean_true(self):
        # when
        result = eval_str("(str true)", create_builtins_module())
        # then
        self.assertEqual("true", result)

    def test_str_stringifies_boolean_false(self):
        # when
        result = eval_str("(str false)", create_builtins_module())
        # then
        self.assertEqual("false", result)

    def test_str_stringifies_boolean_variable(self):
        # when
        result = eval_str("(let (a true) (str a))", create_builtins_module())
        # then
        self.assertEqual("true", result)
