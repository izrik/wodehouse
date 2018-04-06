#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from wodehouse import eval_str, create_default_state, w_print, WList


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
        state['onetwothree'] = lambda *args: 123
        # when
        result = eval_str('(onetwothree)', state)
        # then
        self.assertEqual(123, result)

    def test_evals_strings_dquote(self):
        self.assertEqual('str', eval_str('"str"'))

    def test_evals_strings_squote(self):
        self.assertEqual('str', eval_str("'str'"))

    def test_evals_strings_dquote_in_squote(self):
        self.assertEqual('str"str', eval_str('\'str"str\''))

    def test_evals_strings_dquote_in_dquote(self):
        self.assertEqual('str"str', eval_str('"str\\"str"'))

    def test_evals_strings_squote_in_dquote(self):
        self.assertEqual("str'str", eval_str('"str\'str"'))

    def test_evals_strings_squote_in_squote(self):
        self.assertEqual("str'str", eval_str('\'str\\\'str\''))

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
        state['print'] = lambda x: w_print(x, printer=printer)
        # when
        result = eval_str('(print "Hello, world!")', state)
        # then
        self.assertEqual("Hello, world!", result)

    def test_prints_integer(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = lambda x: w_print(x, printer=printer)
        # when
        result = eval_str('(print 123)', state)
        # then
        printer.assert_called_once_with(123)
        self.assertEqual(123, result)

    def test_prints_string(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = lambda x: w_print(x, printer=printer)
        # when
        result = eval_str('(print "Hello, world!")', state)
        # then
        printer.assert_called_once_with('Hello, world!')
        self.assertEqual('Hello, world!', result)

    def test_prints_escaped_chars_correctly(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = lambda x: w_print(x, printer=printer)
        # when
        result = eval_str('(print "newline\\ncreturn\\rtab\\t")', state)
        # then
        printer.assert_called_once_with('newline\ncreturn\rtab\t')
        self.assertEqual('newline\ncreturn\rtab\t', result)

    def test_prints_empty_list(self):
        # given
        printer = Mock()
        state = create_default_state()
        state['print'] = lambda x: w_print(x, printer=printer)
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
        state['print'] = lambda x: w_print(x, printer=printer)
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

    def test_quotes_string(self):
        # when
        result = eval_str('(quote "asdf")')
        # then
        self.assertEqual("asdf", result)

    def test_quotes_empty_list(self):
        # when
        result = eval_str('(quote ())')
        # then
        self.assertEqual([], result)
        self.assertEqual(WList(), result)

    def test_quotes_list(self):
        # when
        result = eval_str('(quote (1 2 "three"))')
        # then
        self.assertEqual([1, 2, "three"], result)


if __name__ == '__main__':
    unittest.main()
