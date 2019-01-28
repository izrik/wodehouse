from unittest import TestCase

from functions.exec_src import w_exec_src
from functions.scope import create_builtins_module
from macros.define import Define
from macros.import_ import Import
from wtypes.function import WFunction
from wtypes.scope import WScope
from wtypes.symbol import WSymbol


class StaticLoader(Import.DefaultLoader):
    def __init__(self, s):
        self.s = s

    def load(self, module_name):
        return self.s


class ImportTest(TestCase):

    def test_import_imports_names(self):
        # given
        loader = StaticLoader("(define x 1) (define y 2)")

        bm = WScope({
            'import': Import(loader=loader),
            'define': Define(),
        })
        # when
        result = w_exec_src("(import file x)", filename="<test>",
                            builtins_module=bm)
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(6, len(result))
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
        loader = StaticLoader("(define x 'y) (define y 2)")

        bm = create_builtins_module()
        bm['import'] = Import(loader=loader)
        # when
        result = w_exec_src("(import file x)", filename="<test>",
                            builtins_module=bm)
        # then
        self.assertIsInstance(result, WScope)
        self.assertIn('x', result)
        self.assertEqual(WSymbol.get('y'), result['x'])
        self.assertNotIn('y', result)

    def test_defining_names_in_importing_files_not_affect_imported_files(self):
        # given
        loader = StaticLoader("""
                (define x
                (lambda () y))

                (define y 2)
            """)

        bm = create_builtins_module()
        bm['import'] = Import(loader=loader)
        # when
        result = w_exec_src("(import file x) (define y 3) (define z (x))",
                            filename="<test>", builtins_module=bm)
        # then
        self.assertIsInstance(result, WScope)
        self.assertIn('x', result)
        self.assertIsInstance(result['x'], WFunction)
        self.assertIn('y', result)
        self.assertEqual(3, result['y'])
        self.assertIn('z', result)
        self.assertEqual(2, result['z'])
