from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.symbol import WSymbol


class GetTypeTest(TestCase):

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
