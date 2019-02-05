from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.magic_function import WMagicFunction
from wtypes.number import WNumber
from wtypes.symbol import WSymbol


class MapTest(TestCase):

    def test_maps_with_named_function(self):
        # when
        result = eval_str(
            "(map car '((1 2 3) (a b c) (\"a\" \"b\" \"c\")))",
            create_builtins_module())
        # then
        self.assertEqual([1, WSymbol.get('a'), 'a'], result)

    def test_maps_with_lambda(self):
        # when
        result = eval_str("(map (lambda (x) (* x x)) '(1 2 3 4 5))",
                          create_builtins_module())
        # then
        self.assertEqual([1, 4, 9, 16, 25], result)

    def test_maps_multiple_lists_and_arguments(self):
        # when
        result = eval_str("(map (lambda (x y) (* x y)) '(1 2 3) '(4 5 6))",
                          create_builtins_module())
        # then
        self.assertEqual([4, 10, 18], result)

    def test_map_single_arg_calculates_correctly(self):
        # given
        bm = create_builtins_module()

        def sqr(x):
            y = x.value
            return WNumber(y * y)

        bm['sqr'] = WMagicFunction(sqr, bm, name='sqr')
        # when
        result = eval_str("(map sqr '(1 2 3 4 5))", bm)
        # then
        self.assertEqual([1, 4, 9, 16, 25], result)

    def test_map_double_arg_calculates_correctly(self):
        # given
        bm = create_builtins_module()

        def abc(a, b):
            a = a.value
            b = b.value
            return WNumber(a * a + b * b)

        bm['abc'] = WMagicFunction(abc, bm, name='abc')
        # when
        result = eval_str("(map abc '(1 2 3 4 5) '(2 2 2 2 2))", bm)
        # then
        self.assertEqual([5, 8, 13, 20, 29], result)

    def test_map_multi_args_uneven_list_result_matches_shortest_length(self):
        # given
        bm = create_builtins_module()

        def abc(a, b):
            a = a.value
            b = b.value
            return WNumber(a * a + b * b)

        bm['abc'] = WMagicFunction(abc, bm, name='abc')
        # when
        result = eval_str("(map abc '(1 2 3 4 5) '(2 2 2))", bm)
        # then
        self.assertEqual([5, 8, 13], result)

    def test_map_empty_list_yields_empty_list(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str("(map (lambda (x) (* x x)) '())", bm)
        # then
        self.assertEqual([], result)
