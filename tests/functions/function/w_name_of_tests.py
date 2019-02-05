from unittest import TestCase

from functions.eval import eval_str
from functions.function import w_name_of
from modules.builtins import create_builtins_module
from wtypes.function import WFunction
from wtypes.list import WList
from wtypes.string import WString


class NameOfTest(TestCase):

    def test_name_of_magic_function(self):
        # given
        bm = create_builtins_module()
        # when
        result = w_name_of(bm['str'])
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("str", result)
        # when
        result = eval_str("(name_of str)", bm)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("str", result)

    def test_name_of_named_regular_function(self):
        # given
        bm = create_builtins_module()
        f = WFunction(WList(), WList(), enclosing_scope=bm)
        f.name = WString('f')
        bm['f'] = f
        # when
        result = w_name_of(bm['f'])
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("f", result)
        # when
        result = eval_str("(name_of f)", bm)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("f", result)

    def test_name_of_unnamed_regular_function(self):
        # given
        bm = create_builtins_module()
        f = WFunction(WList(), WList(), enclosing_scope=bm)
        bm['f'] = f
        # when
        result = w_name_of(bm['f'])
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("<unnamed_function>", result)
        # when
        result = eval_str("(name_of f)", bm)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("<unnamed_function>", result)

    def test_name_of_magic_macro(self):
        # given
        bm = create_builtins_module()
        # when
        result = w_name_of(bm['import'])
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("import", result)
        # when
        result = eval_str("(name_of import)", bm)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("import", result)

    # TODO: non-magic macros, with and without names
