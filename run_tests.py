#!/usr/bin/env python

import unittest
from unittest.mock import Mock

import functions.eval
from functions.eval import w_eval, eval_str
from functions.exec_src import w_exec_src
from functions.scope import create_global_scope, create_module_scope
from wtypes.function import WFunction
from functions.io import w_print
from wtypes.magic_function import WMagicFunction
from functions.read import parse
from macros.define import Define
from macros.import_ import Import
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.scope import WScope
from wtypes.stream import WStream
from wtypes.string import WString
from wtypes.symbol import WSymbol


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

    def test_print_function(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print "Hello, world!")', scope)
        # then
        self.assertEqual("Hello, world!", result)

    def test_prints_integer(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print 123)', scope)
        # then
        printer.assert_called_once_with(123)
        self.assertEqual(123, result)

    def test_prints_string(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(
            lambda x: w_print(x, printer=printer),
            enclosing_scope=scope)
        # when
        result = eval_str('(print "Hello, world!")', scope)
        # then
        printer.assert_called_once_with('Hello, world!')
        self.assertEqual('Hello, world!', result)

    def test_prints_escaped_chars_correctly(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print "newline\\ncreturn\\rtab\\t")', scope)
        # then
        printer.assert_called_once_with('newline\ncreturn\rtab\t')
        self.assertEqual('newline\ncreturn\rtab\t', result)

    def test_prints_empty_list(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print (quote ()))', scope)
        # then
        printer.assert_called_once_with([])
        printer.assert_called_once_with(WList())
        self.assertEqual(result, [])
        self.assertEqual(result, WList())

    def test_prints_list(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print (quote (1 2 "three")))', scope)
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
        result = eval_str("(type 123)", create_global_scope())
        # then
        self.assertIs(WSymbol.get("Number"), result)

    def test_gets_type_of_string(self):
        # when
        result = eval_str("(type \"abc\")", create_global_scope())
        # then
        self.assertIs(WSymbol.get("String"), result)

    def test_gets_type_of_symbol(self):
        # when
        result = eval_str("(type 'a)", create_global_scope())
        # then
        self.assertIs(WSymbol.get("Symbol"), result)

    def test_gets_type_of_list(self):
        # when
        result = eval_str("(type '())", create_global_scope())
        # then
        self.assertIs(WSymbol.get("List"), result)

    def test_gets_type_of_function(self):
        # when
        result = eval_str("(type (lambda () 1))", create_global_scope())
        # then
        self.assertIs(WSymbol.get("Function"), result)

    def test_gets_type_of_magic_function(self):
        # when
        result = eval_str("(type list)", create_global_scope())
        # then
        self.assertIs(WSymbol.get("MagicFunction"), result)

    # TODO: create anonymous macros
    # def test_gets_type_of_macro(self):
    #     # when
    #     result = eval_str("(type ???)", create_default_scope())
    #     # then
    #     self.assertIs(WSymbol.get("Macro"), result)

    def test_gets_type_of_magic_macro(self):
        # when
        result = eval_str("(type let)", create_global_scope())
        # then
        self.assertIs(WSymbol.get("MagicMacro"), result)

    def test_lambda_creates_wfunction(self):
        # when
        result = eval_str("(lambda (x) 123)", create_global_scope())
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_parameters)
        self.assertEqual([WSymbol.get('x')], result.parameters)
        self.assertEqual(123, result.expr)

    def test_lambda_encloses_values(self):
        # given
        scope = create_global_scope()
        # when
        result = eval_str("(lambda (x) (* x x))", scope)
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_parameters)
        self.assertEqual([WSymbol.get('x')], result.parameters)
        times = WSymbol.get('*')
        x = WSymbol.get('x')
        self.assertEqual([times, x, x], result.expr)

    def test_wfunction_can_be_called(self):
        # when
        result = eval_str("((lambda (x) (* x x)) 4)", create_global_scope())
        # then
        self.assertEqual(16, result)

    def test_wfunctions_can_be_used_in_the_scope(self):
        # given
        scope = create_global_scope()
        scope['sqr'] = eval_str("(lambda (x) (* x x))", scope)
        # expect
        self.assertEqual(25, eval_str("(sqr 5)", scope))
        self.assertEqual(81, eval_str("(sqr 9)", scope))

    def test_str_stringifies_numbers(self):
        # when
        result = eval_str("(str 123)", create_global_scope())
        # then
        self.assertEqual("123", result)

    def test_str_strings_are_unchanged(self):
        # when
        result = eval_str("(str \"123\")", create_global_scope())
        # then
        self.assertEqual("123", result)

    def test_str_stringifies_lists(self):
        # when
        result = eval_str("(str (list 1 2 3))", create_global_scope())
        # then
        self.assertEqual("(1 2 3)", result)

    def test_str_stringifies_quoted_lists(self):
        # when
        result = eval_str("(str '(1 2 3))", create_global_scope())
        # then
        self.assertEqual("(1 2 3)", result)

    def test_str_stringifies_symbols(self):
        # when
        result = eval_str("(str 'asdf)", create_global_scope())
        # then
        self.assertEqual("asdf", result)

    def test_str_stringifies_quoted_symbols(self):
        # when
        result = eval_str("(str ''asdf)", create_global_scope())
        # then
        self.assertEqual("'asdf", result)

    def test_str_stringifies_lambdas(self):
        # when
        result = eval_str("(str (lambda (x) (* x x)))",
                          create_global_scope())
        # then
        self.assertEqual("(lambda (x) (* x x))", result)

    def test_str_stringifies_magic_functions(self):
        # when
        result = eval_str("(str str)", create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertTrue(result.value.startswith("str"))

    def test_str_stringifies_variables_values(self):
        # when
        result = eval_str("(let (a 123) (str a))", create_global_scope())
        # then
        self.assertEqual("123", result)

    def test_str_stringifies_boolean_true(self):
        # when
        result = eval_str("(str true)", create_global_scope())
        # then
        self.assertEqual("true", result)

    def test_str_stringifies_boolean_false(self):
        # when
        result = eval_str("(str false)", create_global_scope())
        # then
        self.assertEqual("false", result)

    def test_str_stringifies_boolean_variable(self):
        # when
        result = eval_str("(let (a true) (str a))", create_global_scope())
        # then
        self.assertEqual("true", result)

    def test_not_inverts_true_to_false(self):
        # when
        result = eval_str("(not true)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_not_inverts_false_to_true(self):
        # when
        result = eval_str("(not false)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_or_returns_true_if_any_true(self):
        # when
        result = eval_str("(or false true)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(or true false)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(or true true)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_or_returns_false_if_all_false(self):
        # when
        result = eval_str("(or false false)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_and_returns_false_if_any_false(self):
        # when
        result = eval_str("(and false true)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)
        # when
        result = eval_str("(and true false)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)
        # when
        result = eval_str("(and false false)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_and_returns_true_if_all_true(self):
        # when
        result = eval_str("(and true true)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_cond_no_conditions_raises(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "No condition evaluated to true.",
            eval_str,
            "(cond)", create_global_scope())

    def test_cond_condition_is_true_returns_corresponding_retval(self):
        # when
        result = eval_str("(cond (true 'a))", create_global_scope())
        # then
        self.assertEqual(WSymbol.get('a'), result)

    def test_cond_condition_is_false_moves_to_next_condition(self):
        # when
        result = eval_str("(cond (false 'a) (true 'b))",
                          create_global_scope())
        # then
        self.assertEqual(WSymbol.get('b'), result)

    def test_cond_condition_is_true_evaluates_true_side(self):
        evaled = False

        def f():
            nonlocal evaled
            evaled = True
            return WSymbol.get('f')

        scope = create_global_scope()
        scope['f'] = WMagicFunction(f, scope)

        # when
        result = eval_str("(cond (true (f)))",
                          scope)
        # then
        self.assertEqual(WSymbol.get('f'), result)
        self.assertTrue(evaled)

    def test_cond_condition_is_false_does_not_evaluate_prior_retvals(self):
        evaled1 = False
        evaled2 = False

        def f1():
            nonlocal evaled1
            evaled1 = True
            return WSymbol.get('f1')

        def f2():
            nonlocal evaled2
            evaled2 = True
            return WSymbol.get('f2')

        scope = create_global_scope()
        scope['f1'] = WMagicFunction(f1, scope)
        scope['f2'] = WMagicFunction(f2, scope)

        # when
        result = eval_str("(cond (false (f1)) (true (f2)))",
                          scope)
        # then
        self.assertEqual(WSymbol.get('f2'), result)
        self.assertFalse(evaled1)
        self.assertTrue(evaled2)

    def test_cond_condition_is_true_does_not_evaluate_later_retvals(self):
        evaled1 = False
        evaled2 = False

        def f1():
            nonlocal evaled1
            evaled1 = True
            return WSymbol.get('f1')

        def f2():
            nonlocal evaled2
            evaled2 = True
            return WSymbol.get('f2')

        scope = create_global_scope()
        scope['f1'] = WMagicFunction(f1, scope)
        scope['f2'] = WMagicFunction(f2, scope)

        # when
        result = eval_str("(cond (true (f1)) (false (f2)))",
                          scope)
        # then
        self.assertEqual(WSymbol.get('f1'), result)
        self.assertTrue(evaled1)
        self.assertFalse(evaled2)

    # TODO: test cond with various levels of quoting

    def test_if_condition_is_true_returns_first_retval(self):
        # when
        result = eval_str("(if (< 2 3) 4 5)",
                          create_global_scope())
        # then
        self.assertEqual(4, result)

    def test_if_condition_is_false_returns_second_retval(self):
        # when
        result = eval_str("(if (> 2 3) 4 5)",
                          create_global_scope())
        # then
        self.assertEqual(5, result)

    def test_less_than_returns_true_for_lesser(self):
        # when
        result = eval_str("(< 1 2)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_less_than_returns_false_for_greater(self):
        # when
        result = eval_str("(< 2 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_less_than_returns_false_for_equal(self):
        # when
        result = eval_str("(< 1 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_leq_returns_true_for_lesser(self):
        # when
        result = eval_str("(<= 1 2)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_leq_returns_false_for_greater(self):
        # when
        result = eval_str("(<= 2 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_leq_returns_true_for_equal(self):
        # when
        result = eval_str("(<= 1 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_greater_than_returns_false_for_lesser(self):
        # when
        result = eval_str("(> 1 2)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_greater_than_returns_true_for_greater(self):
        # when
        result = eval_str("(> 2 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_greater_than_returns_false_for_equal(self):
        # when
        result = eval_str("(> 1 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_geq_returns_false_for_lesser(self):
        # when
        result = eval_str("(>= 1 2)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_geq_returns_true_for_greater(self):
        # when
        result = eval_str("(>= 2 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_geq_returns_true_for_equal(self):
        # when
        result = eval_str("(>= 1 1)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_new_scope_creates_scope_object(self):
        # when
        result = eval_str("(new_scope)", create_global_scope())
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(0, len(result))

    def test_new_scope_with_empty_list_for_args_creates_scope_object(self):
        # when
        result = eval_str("(new_scope '())", create_global_scope())
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(0, len(result))

    def test_new_scope_args_become_keys_and_values(self):
        # when
        result = eval_str("(new_scope '((a 1) (b 2)))", create_global_scope())
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(2, len(result))
        self.assertIn('a', result)
        self.assertEqual(1, result['a'])
        self.assertIn('b', result)
        self.assertEqual(2, result['b'])

    def test_get_gets_value_by_key(self):
        # when
        result = eval_str("(get (new_scope '((a 1) (b 2))) 'a)",
                          create_global_scope())
        # then
        self.assertEqual(1, result)
        # when
        result = eval_str("(get (new_scope '((a 1) (b 2))) 'b)",
                          create_global_scope())
        # then
        self.assertEqual(2, result)

    def test_new_scope_within_create_scope_object_with_enclosing_scope(self):
        # given
        p = WScope({'a': 3, 'b': 4, 'c': 5})
        gs = create_global_scope()
        gs['p'] = p
        # when
        result = eval_str("(new_scope_within p '((a 1) (b 2)))", gs)
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(3, len(result))
        self.assertIn('a', result)
        self.assertEqual(1, result['a'])
        self.assertIn('b', result)
        self.assertEqual(2, result['b'])
        self.assertIn('c', result)
        self.assertNotIn('c', result.dict.keys())
        self.assertIn('c', result.enclosing_scope)
        self.assertEqual(5, result.enclosing_scope['c'])
        # expect
        p2 = result
        self.assertEqual(1, eval_str("a", p2))
        self.assertEqual(2, eval_str("b", p2))
        self.assertEqual(5, eval_str("c", p2))

    def test_in_returns_false_if_item_present(self):
        # when
        result = eval_str("(in 'a '(a))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'a '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'b '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'c '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_in_returns_false_if_item_not_present(self):
        # when
        result = eval_str("(in 'f '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

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

    def test_maps_with_named_function(self):
        # when
        result = eval_str(
            "(map car '('(1 2 3) '(a b c) '(\"a\" \"b\" \"c\")))",
            create_global_scope())
        # then
        self.assertEqual([1, WSymbol.get('a'), 'a'], result)

    def test_maps_with_lambda(self):
        # when
        result = eval_str("(map (lambda (x) (* x x)) '(1 2 3 4 5))",
                          create_global_scope())
        # then
        self.assertEqual([1, 4, 9, 16, 25], result)

    def test_maps_multiple_lists_and_arguments(self):
        # when
        result = eval_str("(map (lambda (x y) (* x y)) '(1 2 3) '(4 5 6))",
                          create_global_scope())
        # then
        self.assertEqual([4, 10, 18], result)

    def test_parses_w_eval(self):
        # given
        source = functions.eval._eval_source
        # when
        result = parse(source)
        # then
        self.assertNotEqual([], result)

    def test_compiles_w_eval(self):
        # given
        eval_source = functions.eval._eval_source
        parsed_eval = parse(eval_source)
        scope = create_global_scope()
        scope['scope'] = scope
        # when
        compiled_eval = w_eval(parsed_eval, scope)
        # then
        self.assertIsInstance(compiled_eval, WFunction)

    def test_compiled_w_eval_evals_things(self):
        # given
        eval_source = functions.eval._eval_source
        parsed_eval = parse(eval_source)
        scope = create_global_scope()
        scope['scope'] = scope
        compiled_eval = w_eval(parsed_eval, scope)
        scope['w_eval'] = compiled_eval
        # when
        result = eval_str('(w_eval 2 scope)', scope)
        # then
        self.assertEqual(2, result)

    def test_read_file_reads_files(self):
        # when
        result = eval_str("(read_file \"input2.txt\")", create_global_scope())
        # then
        self.assertEqual("( 123 )\n", result)

    def test_assert_raises_exception_on_false(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "Assertion failed: \"false\"",
            eval_str,
            "(assert false)", create_global_scope())

    def test_assert_raises_exception_on_false_expr(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "Assertion failed: \"\\(< 3 1\\)\"",
            eval_str,
            "(assert (< 3 1))", create_global_scope())

    def test_assert_returns_true_on_true(self):
        # when
        result = eval_str("(assert (< 1 2))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_assert_returns_arg_on_non_boolean(self):
        # when
        result = eval_str("(assert \"abc\")", create_global_scope())
        # then
        self.assertEqual("abc", result)

    def test_define_in_module_adds_to_module_scope(self):
        # given
        gs = create_global_scope()
        scope = create_module_scope(enclosing_scope=gs)
        # when
        result = eval_str("(define x 3)", scope)
        # then
        self.assertEqual(3, result)
        self.assertIn(WSymbol.get('x'), scope)
        self.assertEqual(WNumber(3), scope['x'])

    def test_plus_adds_numbers(self):
        # when
        result = eval_str("(+ 1 2 3 4)", create_global_scope())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)

    def test_plus_concatenates_strings(self):
        # when
        result = eval_str("(+ \"one\" \"two\" \"three\")",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("onetwothree", result)

    def test_plus_interprets_single_list_arg_as_varargs(self):
        # when
        result = eval_str("(+ (list 1 2 3 4))", create_global_scope())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)

    def test_format_interpolates_arguments(self):
        # when
        result = eval_str("(format \"one {} three\" \"two\")",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("one two three", result)

    def test_format_interprets_double_braces_as_escaped(self):
        # when
        result = eval_str("(format \"abc {{ def\")", create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("abc { def", result)

    def test_format_stringifies_arguments(self):
        # when
        result = eval_str("(format \"a{}b{}c{}d\" 1 true +)",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a1btruec+d", result)

    def test_raise_raises(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "this is the description",
            eval_str,
            "(raise \"this is the description\")", create_global_scope())

    def test_stream_creates_stream_object(self):
        # when
        result = eval_str("(stream \"abc\")", create_global_scope())
        # then
        self.assertIsInstance(result, WStream)
        self.assertEqual("abc", result.s)

    def test_has_chars_on_empty_stream_returns_false(self):
        # when
        result = eval_str("(has_chars (stream \"\"))", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)

    def test_has_chars_on_non_empty_stream_returns_true(self):
        # when
        result = eval_str("(has_chars (stream \"abc\"))",
                          create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_get_next_char_gets_next_char(self):
        # when
        result = eval_str("(get_next_char (stream \"abc\"))",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a", result)

    def test_get_next_char_advances_position(self):
        # given
        s = WStream("abc")
        scope = create_global_scope()
        scope['s'] = s
        # precondition
        self.assertEqual(eval_str("(get_next_char s)", scope), "a")
        # expect
        self.assertEqual(eval_str("(get_next_char s)", scope), "b")
        self.assertEqual(eval_str("(get_next_char s)", scope), "c")
        # then
        self.assertIs(WBoolean.false, eval_str("(has_chars s)", scope))

    def test_get_next_char_after_end_of_stream_raises(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "No more characters in the stream.",
            eval_str,
            "(get_next_char (stream \"\"))", create_global_scope())

    def test_peek_returns_next_char(self):
        # when
        result = eval_str("(peek (stream \"abc\"))", create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a", result)

    def test_peek_does_not_advance_position(self):
        # given
        s = WStream("abc")
        scope = create_global_scope()
        scope['s'] = s
        # precondition
        self.assertEqual(eval_str("(peek s)", scope), "a")
        # expect
        self.assertEqual(eval_str("(peek s)", scope), "a")
        self.assertEqual(eval_str("(peek s)", scope), "a")

    def test_exec_execs_things(self):
        i = [0]

        def side_effect():
            i[0] += 1
            return WNumber(-1)

        scope = create_global_scope()
        scope['side_effect'] = WMagicFunction(side_effect,
                                              enclosing_scope=scope)
        # when
        eval_str("(exec (side_effect) (side_effect))", scope)
        # then
        self.assertEqual(2, i[0])

    def test_exec_returns_the_last_expr(self):
        # when
        result = eval_str("(exec 2 3 5 7 11)", create_global_scope())
        # then
        self.assertEqual(11, result)

    def test_call_macro_returns_number(self):
        # when
        result = eval_str("(if true 1 2)", create_global_scope())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_call_macro_returns_empty_list(self):
        # when
        result = eval_str("(if true '() 2)", create_global_scope())
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)

    def test_call_nested_macro_returns_empty_list(self):
        # when
        result = eval_str("(if true (if true '() 2) 3)",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)

    def test_w_exec_src_execs_src_and_returns_ms(self):
        # given
        gs = WScope()
        # when
        result = w_exec_src(src="", filename="<test>", enclosing_scope=gs)
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WScope)
        self.assertEqual(4, len(result))
        self.assertIn('__module__', result)
        self.assertIs(result, result['__module__'])
        self.assertIn('__global__', result)
        self.assertIs(gs, result['__global__'])
        self.assertIn('__name__', result)
        self.assertEqual("<test>", result['__name__'])
        self.assertIn('__file__', result)
        self.assertEqual("<test>", result['__file__'])

    def test_import_imports_names(self):
        # given
        def loader(filename):
            return "(define x 1) (define y 2)"

        gs = WScope({
            'import': Import(loader=loader),
            'define': Define(),
        })
        # when
        result = w_exec_src("(import \"file\" x)", filename="<test>",
                            enclosing_scope=gs)
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(8, len(result))
        self.assertIn('__module__', result)
        self.assertIs(result, result['__module__'])
        self.assertIn('file', result)
        self.assertIsInstance(result['file'], WScope)
        self.assertIn('x', result['file'])
        self.assertIn('y', result['file'])
        self.assertIn('x', result)
        self.assertEqual(1, result['x'])
        self.assertNotIn('y', result)

    def test_import_imported_names_quoted_symbols_are_not_resolved(self):
        # given
        def loader(filename):
            return "(define x 'y) (define y 2)"

        gs = create_global_scope()
        gs['import'] = Import(loader=loader)
        # when
        result = w_exec_src("(import \"file\" x)", filename="<test>",
                            enclosing_scope=gs)
        # then
        self.assertIsInstance(result, WScope)
        self.assertIn('x', result)
        self.assertEqual(WSymbol.get('y'), result['x'])
        self.assertNotIn('y', result)

    def test_defining_names_in_importing_files_not_affect_imported_files(self):
        # given
        def loader(filename):
            return """
                (define x
                (lambda () y))

                (define y 2)
            """

        gs = create_global_scope()
        gs['import'] = Import(loader=loader)
        # when
        result = w_exec_src("(import \"file\" x) (define y 3) (define z (x))",
                            filename="<test>", enclosing_scope=gs)
        # then
        self.assertIsInstance(result, WScope)
        self.assertIn('x', result)
        self.assertIsInstance(result['x'], WFunction)
        self.assertIn('y', result)
        self.assertEqual(3, result['y'])
        self.assertIn('z', result)
        self.assertEqual(2, result['z'])

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

    def test_gets_type_of_exception(self):
        # when
        result = eval_str("(type (exception))", create_global_scope())
        # then
        self.assertIs(WSymbol.get("Exception"), result)

    def test_gets_type_of_exception_with_message(self):
        # when
        result = eval_str("(type (exception \"message\"))",
                          create_global_scope())
        # then
        self.assertIs(WSymbol.get("Exception"), result)

    def test_map_single_arg_calculates_correctly(self):
        # given
        gs = create_global_scope()

        def sqr(x):
            y = x.value
            return WNumber(y * y)

        gs['sqr'] = WMagicFunction(sqr, gs, name='sqr')
        # when
        result = eval_str("(map sqr '(1 2 3 4 5))", gs)
        # then
        self.assertEqual([1, 4, 9, 16, 25], result)

    def test_map_double_arg_calculates_correctly(self):
        # given
        gs = create_global_scope()

        def abc(a, b):
            a = a.value
            b = b.value
            return WNumber(a * a + b * b)

        gs['abc'] = WMagicFunction(abc, gs, name='abc')
        # when
        result = eval_str("(map abc '(1 2 3 4 5) '(2 2 2 2 2))", gs)
        # then
        self.assertEqual([5, 8, 13, 20, 29], result)

    def test_map_multi_args_uneven_list_result_matches_shortest_length(self):
        # given
        gs = create_global_scope()

        def abc(a, b):
            a = a.value
            b = b.value
            return WNumber(a * a + b * b)

        gs['abc'] = WMagicFunction(abc, gs, name='abc')
        # when
        result = eval_str("(map abc '(1 2 3 4 5) '(2 2 2))", gs)
        # then
        self.assertEqual([5, 8, 13], result)

    def test_map_empty_list_yields_empty_list(self):
        # given
        gs = create_global_scope()
        # when
        result = eval_str("(map (lambda (x) (* x x)) '())", gs)
        # then
        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()
