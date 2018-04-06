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


if __name__ == '__main__':
    unittest.main()
