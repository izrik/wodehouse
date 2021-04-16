import unittest

from wodehouse import main


class MainTest(unittest.TestCase):
    def test_command(self):
        from wtypes.module import WModule
        from wtypes.string import WString
        from wtypes.symbol import WSymbol
        # when
        result = main(['-c', '123'])
        # then
        self.assertIsInstance(result, WModule)
        self.assertIsNone(result.enclosing_scope)
        self.assertEqual(result.name, '__main__')

        s_module = WSymbol.get('__module__')
        self.assertIn(s_module, result.dict)
        self.assertIsInstance(result.dict[s_module], WModule)
        self.assertIs(result.dict[s_module], result)

        s_name = WSymbol.get('__name__')
        self.assertIn(s_name, result.dict)
        self.assertIsInstance(result.dict[s_name], WString)
        self.assertEqual(result.dict[s_name], '__main__')

        s_file = WSymbol.get('__file__')
        self.assertIn(s_file, result.dict)
        self.assertIsInstance(result.dict[s_file], WString)
        self.assertEqual(result.dict[s_file], '<string>')

        s_builtins = WSymbol.get('__builtins__')
        self.assertIn(s_builtins, result.dict)
        self.assertIsInstance(result.dict[s_builtins], WModule)
