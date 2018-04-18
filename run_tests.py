#!/usr/bin/env python

import unittest
from unittest.mock import Mock

import wodehouse
from wodehouse import eval_str, create_default_state, w_print, WList, \
    WSymbol, WFunction, WMagicFunction, WString, WBoolean, WState, parse, \
    create_file_level_state, WNumber


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

    def test_gets_type_of_function(self):
        # when
        result = eval_str("(type (lambda () 1))", create_default_state())
        # then
        self.assertIs(WSymbol.get("Function"), result)

    def test_gets_type_of_magic_function(self):
        # when
        result = eval_str("(type list)", create_default_state())
        # then
        self.assertIs(WSymbol.get("MagicFunction"), result)

    # TODO: create anonymous macros
    # def test_gets_type_of_macro(self):
    #     # when
    #     result = eval_str("(type ???)", create_default_state())
    #     # then
    #     self.assertIs(WSymbol.get("Macro"), result)

    def test_gets_type_of_magic_macro(self):
        # when
        result = eval_str("(type let)", create_default_state())
        # then
        self.assertIs(WSymbol.get("MagicMacro"), result)

    def test_lambda_creates_wfunction(self):
        # when
        result = eval_str("(lambda (x) 123)", create_default_state())
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_args)
        self.assertEqual([WSymbol.get('x')], result.args)
        self.assertEqual(123, result.expr)

    def test_lambda_encloses_values(self):
        # given
        state = create_default_state()
        # when
        result = eval_str("(lambda (x) (* x x))", state)
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_args)
        self.assertEqual([WSymbol.get('x')], result.args)
        times = state['*']
        x = WSymbol.get('x')
        self.assertEqual([times, x, x], result.expr)

    def test_wfunction_can_be_called(self):
        # when
        result = eval_str("((lambda (x) (* x x)) 4)", create_default_state())
        # then
        self.assertEqual(16, result)

    def test_wfunctions_can_be_used_in_the_state(self):
        # given
        state = create_default_state()
        state['sqr'] = eval_str("(lambda (x) (* x x))", state)
        # expect
        self.assertEqual(25, eval_str("(sqr 5)", state))
        self.assertEqual(81, eval_str("(sqr 9)", state))

    def test_str_stringifies_numbers(self):
        # when
        result = eval_str("(str 123)", create_default_state())
        # then
        self.assertEqual("123", result)

    def test_str_strings_are_unchanged(self):
        # when
        result = eval_str("(str \"123\")", create_default_state())
        # then
        self.assertEqual("123", result)

    def test_str_stringifies_lists(self):
        # when
        result = eval_str("(str (list 1 2 3))", create_default_state())
        # then
        self.assertEqual("(1 2 3)", result)

    def test_str_stringifies_quoted_lists(self):
        # when
        result = eval_str("(str '(1 2 3))", create_default_state())
        # then
        self.assertEqual("(1 2 3)", result)

    def test_str_stringifies_symbols(self):
        # when
        result = eval_str("(str 'asdf)", create_default_state())
        # then
        self.assertEqual("asdf", result)

    def test_str_stringifies_quoted_symbols(self):
        # when
        result = eval_str("(str ''asdf)", create_default_state())
        # then
        self.assertEqual("'asdf", result)

    def test_str_stringifies_lambdas(self):
        # when
        result = eval_str("(str (lambda (x) (* x x)))",
                          create_default_state())
        # then
        self.assertEqual("(lambda (x) (* x x))", result)

    def test_str_stringifies_magic_functions(self):
        # when
        result = eval_str("(str str)", create_default_state())
        # then
        self.assertIsInstance(result, WString)
        self.assertTrue(result.value.startswith("str"))

    def test_str_stringifies_variables_values(self):
        # when
        result = eval_str("(let a 123 str a)", create_default_state())
        # then
        self.assertEqual("123", result)

    def test_str_stringifies_boolean_true(self):
        # when
        result = eval_str("(str true)", create_default_state())
        # then
        self.assertEqual("true", result)

    def test_str_stringifies_boolean_false(self):
        # when
        result = eval_str("(str false)", create_default_state())
        # then
        self.assertEqual("false", result)

    def test_str_stringifies_boolean_variable(self):
        # when
        result = eval_str("(let a true str a)", create_default_state())
        # then
        self.assertEqual("true", result)

    def test_not_inverts_true_to_false(self):
        # when
        result = eval_str("(not true)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_not_inverts_false_to_true(self):
        # when
        result = eval_str("(not false)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_cond_no_conditions_raises(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "No condition evaluated to true.",
            eval_str,
            "(cond)", create_default_state())

    def test_cond_condition_is_true_returns_corresponding_retval(self):
        # when
        result = eval_str("(cond (true 'a))", create_default_state())
        # then
        self.assertIs(WSymbol.get('a'), result)

    def test_cond_condition_is_false_moves_to_next_condition(self):
        # when
        result = eval_str("(cond (false 'a) (true 'b))",
                          create_default_state())
        # then
        self.assertIs(WSymbol.get('b'), result)

    def test_if_condition_is_true_returns_first_retval(self):
        # when
        result = eval_str("(if (< 2 3) 4 5)",
                          create_default_state())
        # then
        self.assertEqual(4, result)

    def test_if_condition_is_false_returns_second_retval(self):
        # when
        result = eval_str("(if (> 2 3) 4 5)",
                          create_default_state())
        # then
        self.assertEqual(5, result)

    def test_less_than_returns_true_for_lesser(self):
        # when
        result = eval_str("(< 1 2)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_less_than_returns_false_for_greater(self):
        # when
        result = eval_str("(< 2 1)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_less_than_returns_false_for_equal(self):
        # when
        result = eval_str("(< 1 1)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_leq_returns_true_for_lesser(self):
        # when
        result = eval_str("(<= 1 2)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_leq_returns_false_for_greater(self):
        # when
        result = eval_str("(<= 2 1)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_leq_returns_true_for_equal(self):
        # when
        result = eval_str("(<= 1 1)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_greater_than_returns_false_for_lesser(self):
        # when
        result = eval_str("(> 1 2)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_greater_than_returns_true_for_greater(self):
        # when
        result = eval_str("(> 2 1)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_greater_than_returns_false_for_equal(self):
        # when
        result = eval_str("(> 1 1)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_geq_returns_false_for_lesser(self):
        # when
        result = eval_str("(>= 1 2)", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_geq_returns_true_for_greater(self):
        # when
        result = eval_str("(>= 2 1)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_geq_returns_true_for_equal(self):
        # when
        result = eval_str("(>= 1 1)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_new_state_creates_state_object(self):
        # when
        result = eval_str("(new_state)", create_default_state())
        # then
        self.assertIsInstance(result, WState)
        self.assertEqual(0, len(result))

    def test_new_state_with_empty_list_for_args_creates_state_object(self):
        # when
        result = eval_str("(new_state '())", create_default_state())
        # then
        self.assertIsInstance(result, WState)
        self.assertEqual(0, len(result))

    def test_new_state_args_become_keys_and_values(self):
        # when
        result = eval_str("(new_state '((a 1) (b 2)))", create_default_state())
        # then
        self.assertIsInstance(result, WState)
        self.assertEqual(2, len(result))
        self.assertIn('a', result)
        self.assertEqual(1, result['a'])
        self.assertIn('b', result)
        self.assertEqual(2, result['b'])

    def test_get_gets_value_by_key(self):
        # when
        result = eval_str("(get (new_state '((a 1) (b 2))) 'a)",
                          create_default_state())
        # then
        self.assertEqual(1, result)
        # when
        result = eval_str("(get (new_state '((a 1) (b 2))) 'b)",
                          create_default_state())
        # then
        self.assertEqual(2, result)

    def test_new_state_proto_create_state_object_with_prototype(self):
        # given
        p = WState({'a': 3, 'b': 4, 'c': 5})
        state = create_default_state()
        state['p'] = p
        # when
        result = eval_str("(new_state_proto p '((a 1) (b 2)))", state)
        # then
        self.assertIsInstance(result, WState)
        self.assertEqual(3, len(result))
        self.assertIn('a', result)
        self.assertEqual(1, result['a'])
        self.assertIn('b', result)
        self.assertEqual(2, result['b'])
        self.assertIn('c', result)
        self.assertEqual(5, result['c'])

    def test_in_returns_false_if_item_present(self):
        # when
        result = eval_str("(in 'a '(a))", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'a '(a b c))", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'b '(a b c))", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'c '(a b c))", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_in_returns_false_if_item_not_present(self):
        # when
        result = eval_str("(in 'f '(a b c))", create_default_state())
        # then
        self.assertIs(WBoolean.false, result)

    def test_isinstance_returns_true_when_match_number(self):
        # when
        result = eval_str("(isinstance 123 'Number)", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_number_type_list(self):
        # when
        result = eval_str("(isinstance 123 '(Number))", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_string(self):
        # when
        result = eval_str("(isinstance \"abc\" 'String)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_string_type_list(self):
        # when
        result = eval_str("(isinstance \"abc\" '(String))",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_mixed_type_list(self):
        # when
        result = eval_str("(isinstance 123 '(Number String))",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(isinstance \"abc\" '(Number String))",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_function(self):
        # when
        result = eval_str("(isinstance (lambda () 1) 'Function)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_magic_function(self):
        # when
        result = eval_str("(isinstance list 'MagicFunction)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_function_with_magic_func(self):
        # when
        result = eval_str("(isinstance list 'Function)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_boolean(self):
        # when
        result = eval_str("(isinstance (lambda () 1) 'Function)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    # TODO: create anonymous macros
    # def test_isinstance_returns_true_when_match_macro(self):
    #     # when
    #     result = eval_str("(isinstance let 'Macro)",
    #                       create_default_state())
    #     # then
    #     self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_magic_macro(self):
        # when
        result = eval_str("(isinstance let 'MagicMacro)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_macro_with_magic_macro(self):
        # when
        result = eval_str("(isinstance let 'Macro)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_symbol(self):
        # when
        result = eval_str("(isinstance 'a 'Symbol)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_true_when_match_list(self):
        # when
        result = eval_str("(isinstance '(1 2 3) 'List)",
                          create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_isinstance_returns_false_when_does_not_match(self):
        # when
        result = eval_str(
            "(isinstance 123 '(String Symbol Boolean List Function Macro))",
            create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_maps_with_named_function(self):
        # when
        result = eval_str(
            "(map car '('(1 2 3) '(a b c) '(\"a\" \"b\" \"c\")))",
            create_default_state())
        # then
        self.assertEqual([1, WSymbol.get('a'), 'a'], result)

    def test_maps_with_lambda(self):
        # when
        result = eval_str("(map (lambda (x) (* x x)) '(1 2 3 4 5))",
                          create_default_state())
        # then
        self.assertEqual([1, 4, 9, 16, 25], result)

    def test_maps_multiple_lists_and_arguments(self):
        # when
        result = eval_str("(map (lambda (x y) (* x y)) '(1 2 3) '(4 5 6))",
                          create_default_state())
        # then
        self.assertEqual([4, 10, 18], result)

    def test_parses_w_eval(self):
        # given
        source = wodehouse._eval_source
        # when
        result = parse(source)
        # then
        self.assertNotEqual([], result)

    def test_compiles_w_eval(self):
        # given
        eval_source = wodehouse._eval_source
        parsed_eval = parse(eval_source)
        state = create_default_state()
        state['state'] = state
        # when
        compiled_eval = wodehouse.w_eval(parsed_eval, state)
        # then
        self.assertIsInstance(compiled_eval, WFunction)

    def test_compiled_w_eval_evals_things(self):
        # given
        eval_source = wodehouse._eval_source
        parsed_eval = parse(eval_source)
        state = create_default_state()
        state['state'] = state
        compiled_eval = wodehouse.w_eval(parsed_eval, state)
        state['w_eval'] = compiled_eval
        # when
        result = eval_str('(w_eval 2 state)', state)
        # then
        self.assertEqual(2, result)

    def test_read_file_reads_files(self):
        # when
        result = eval_str("(read_file \"input2.txt\")", create_default_state())
        # then
        self.assertEqual("( 123 )\n", result)

    def test_assert_raises_exception_on_false(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "Assertion failed\\.",
            eval_str,
            "(assert false)", create_default_state())

    def test_assert_raises_exception_on_false_expr(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "Assertion failed\\.",
            eval_str,
            "(assert (< 3 1))", create_default_state())

    def test_assert_returns_true_on_true(self):
        # when
        result = eval_str("(assert (< 1 2))", create_default_state())
        # then
        self.assertIs(WBoolean.true, result)

    def test_assert_returns_arg_on_non_boolean(self):
        # when
        result = eval_str("(assert \"abc\")", create_default_state())
        # then
        self.assertEqual("abc", result)

    def test_define_adds_to_fls(self):
        # given
        fls = create_file_level_state()
        state = create_default_state(fls)
        # when
        result = eval_str("(define x 3)", state)
        # then
        self.assertEqual(3, result)
        self.assertIn(WSymbol.get('x'), fls)
        self.assertEqual(WNumber(3), fls['x'])


if __name__ == '__main__':
    unittest.main()
