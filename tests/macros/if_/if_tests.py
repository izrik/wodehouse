from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.control import WRaisedException
from wtypes.exception import WSyntaxError


class IfTest(TestCase):

    def test_if_condition_is_true_returns_first_retval(self):
        # when
        result = eval_str("(if (< 2 3) 4 5)",
                          create_builtins_module())
        # then
        self.assertEqual(4, result)

    def test_if_condition_is_false_returns_second_retval(self):
        # when
        result = eval_str("(if (> 2 3) 4 5)",
                          create_builtins_module())
        # then
        self.assertEqual(5, result)

    def test_too_few_arguments_yields_syntax_error(self):
        # when
        result = eval_str("(if (> 2 3))",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(result.exception.message,
                         'Expected 2 or 3 arguments to if, got 1 instead.')
        self.assertEqual(result.exception.position.line, 1)
        self.assertEqual(result.exception.position.char, 5)

    def test_too_many_arguments_yields_syntax_error(self):
        # when
        result = eval_str("(if (> 2 3) 4 5 6)",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(result.exception.message,
                         'Expected 2 or 3 arguments to if, got 4 instead.')
        self.assertEqual(result.exception.position.line, 1)
        self.assertEqual(result.exception.position.char, 5)
