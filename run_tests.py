#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from wodehouse import eval_str, create_default_state, w_print, WList, \
    WSymbol, WFunction, WMagicFunction


class WodehouseTest(unittest.TestCase):
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
        state = create_default_state()
        state['onetwothree'] = WMagicFunction(lambda *args: 123)
        # when
        result = eval_str('(onetwothree)', state)
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

    def test_print_function(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = WMagicFunction(lambda x: w_print(x, printer=printer))
        # when
        result = eval_str('(print "Hello, world!")', state)
        # then
        self.assertEqual("Hello, world!", result)

    def test_prints_integer(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = WMagicFunction(lambda x: w_print(x, printer=printer))
        # when
        result = eval_str('(print 123)', state)
        # then
        printer.assert_called_once_with(123)
        self.assertEqual(123, result)

    def test_prints_string(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = WMagicFunction(lambda x: w_print(x, printer=printer))
        # when
        result = eval_str('(print "Hello, world!")', state)
        # then
        printer.assert_called_once_with('Hello, world!')
        self.assertEqual('Hello, world!', result)

    def test_prints_escaped_chars_correctly(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = WMagicFunction(lambda x: w_print(x, printer=printer))
        # when
        result = eval_str('(print "newline\\ncreturn\\rtab\\t")', state)
        # then
        printer.assert_called_once_with('newline\ncreturn\rtab\t')
        self.assertEqual('newline\ncreturn\rtab\t', result)

    def test_prints_empty_list(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = WMagicFunction(lambda x: w_print(x, printer=printer))
        # when
        result = eval_str('(print (quote ()))', state)
        # then
        printer.assert_called_once_with([])
        printer.assert_called_once_with(WList())
        self.assertEqual(result, [])
        self.assertEqual(result, WList())

    def test_prints_list(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = WMagicFunction(lambda x: w_print(x, printer=printer))
        # when
        result = eval_str('(print (quote (1 2 "three")))', state)
        # then
        printer.assert_called_once_with([1, 2, "three"])
        self.assertEqual(result, [1, 2, "three"])

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

    def test_gets_type_of_number(self):
        # when
        result = eval_str("(type 123)", create_default_state())
        # then
        self.assertIs(WSymbol.get("Number"), result)

    def test_gets_type_of_string(self):
        # when
        result = eval_str("(type \"abc\")", create_default_state())
        # then
        self.assertIs(WSymbol.get("String"), result)

    def test_gets_type_of_symbol(self):
        # when
        result = eval_str("(type 'a)", create_default_state())
        # then
        self.assertIs(WSymbol.get("Symbol"), result)

    def test_gets_type_of_list(self):
        # when
        result = eval_str("(type '())", create_default_state())
        # then
        self.assertIs(WSymbol.get("List"), result)

    def test_lambda_creates_wfunction(self):
        # when
        result = eval_str("(lambda '(x) '(* x x))", create_default_state())
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_args)
        self.assertEqual([WSymbol.get('x')], result.args)
        times = WSymbol.get('*')
        x = WSymbol.get('x')
        self.assertEqual([times, x, x], result.expr)

    def test_wfunction_can_be_called(self):
        # when
        result = eval_str("((lambda '(x) '(* x x)) 4)", create_default_state())
        # then
        self.assertEqual(16, result)

    def test_wfunctions_can_be_used_in_the_state(self):
        # given
        state = create_default_state()
        state['sqr'] = eval_str("(lambda '(x) '(* x x))", state)
        # expect
        self.assertEqual(25, eval_str("(sqr 5)", state))
        self.assertEqual(81, eval_str("(sqr 9)", state))


if __name__ == '__main__':
    unittest.main()
