from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.list import WList
from wtypes.magic_function import WMagicFunction
from wtypes.number import WNumber


class EvalStringTest(TestCase):

    def test_evals_integers(self):
        # when
        result = eval_str('123', {})
        # then
        self.assertEqual(123, result)

    def test_evals_variables(self):
        # when
        result = eval_str('abc', {'abc': 123})
        # then
        self.assertEqual(123, result)

    def test_calls_functions(self):
        # given
        scope = create_global_scope()
        scope['onetwothree'] = WMagicFunction(lambda *args: WNumber(123),
                                              enclosing_scope=scope)
        # when
        result = eval_str('(onetwothree)', scope)
        # then
        self.assertEqual(123, result)

    def test_evals_strings_dquote(self):
        self.assertEqual('str', eval_str('"str"'))

    def test_evals_strings_dquote_in_dquote(self):
        self.assertEqual('str"str', eval_str('"str\\"str"'))

    def test_evals_strings_newline(self):
        self.assertEqual("\n", eval_str('"\\n"'))

    def test_evals_strings_carriage_return(self):
        self.assertEqual("\r", eval_str('"\\r"'))

    def test_evals_strings_tab(self):
        self.assertEqual("\t", eval_str('"\\t"'))

    def test_quotes_integer(self):
        # when
        result = eval_str('(quote 123)')
        # then
        self.assertEqual(123, result)

    def test_quotes_integer_short_form(self):
        # when
        result = eval_str('(quote 123)')
        # then
        self.assertEqual(123, result)

    def test_quotes_string(self):
        # when
        result = eval_str('(quote "asdf")')
        # then
        self.assertEqual("asdf", result)

    def test_quotes_string_short_form(self):
        # when
        result = eval_str('\'"asdf"')
        # then
        self.assertEqual("asdf", result)

    def test_quotes_empty_list(self):
        # when
        result = eval_str('(quote ())')
        # then
        self.assertEqual([], result)
        self.assertEqual(WList(), result)

    def test_quotes_empty_list_short_form(self):
        # when
        result = eval_str('\'()')
        # then
        self.assertEqual([], result)
        self.assertEqual(WList(), result)

    def test_quotes_list(self):
        # when
        result = eval_str('(quote (1 2 "three"))')
        # then
        self.assertEqual([1, 2, "three"], result)

    def test_quotes_list_short_form(self):
        # when
        result = eval_str('\'(1 2 "three")')
        # then
        self.assertEqual([1, 2, "three"], result)
