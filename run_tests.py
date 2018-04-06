#!/usr/bin/env python

import unittest
from wodehouse import eval_str, create_default_state


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
        # TODO: test the print function without actually writing to stdout
        #       maybe use something like `patch`.
        # when
        result = eval_str('(print "Hello, world!")', create_default_state())
        # then
        self.assertEqual("Hello, world!", result)

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


if __name__ == '__main__':
    unittest.main()
