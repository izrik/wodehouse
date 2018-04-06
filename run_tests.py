#!/usr/bin/env python

import unittest
from wodehouse import eval_str


class WodehouseTest(unittest.TestCase):
    def test_evals_integers(self):
        # given
        input_s = '123'
        # when
        result = eval_str('123', {})
        # then
        self.assertEqual(123, result)


if __name__ == '__main__':
    unittest.main()
