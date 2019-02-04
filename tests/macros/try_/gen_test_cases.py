def gen_py_test_cases_4():
    stmts = [
        {'code': 'a', 's': '{} = 1'},
        {'code': 'r', 's': 'return "{}"'},
        {'code': 'e', 's': 'raise Exception("{}")'}
    ]
    template = \
        '''    def test_py_exception_handling_permutation_{}{}{}{}(self):
        # given
        def x():
            try:
                {}
            except:
                {}
            else:
                {}
            finally:
                {}
            return 0
        # when
        result = x()
        # then
        self.assertTrue(True)
'''
    for code in stmts:
        for exc in stmts:
            for els in stmts:
                for fin in stmts:
                    method = template.format(
                        code['code'], exc['code'], els['code'], fin['code'],
                        code['s'].format('code'),
                        exc['s'].format('exc'),
                        els['s'].format('els'),
                        fin['s'].format('fin'))
                    print(method)


def gen_py_test_cases_3():
    stmts = [
        {'code': 'a', 's': '{} = 1'},
        {'code': 'r', 's': 'return "{}"'},
        {'code': 'e', 's': 'raise Exception("{}")'}
    ]
    template = '''    def test_py_exception_handling_permutation_{}{}{}(self):
        # given
        def x():
            try:
                {}
            except:
                {}
            finally:
                {}
            return 0
        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))
'''
    for code in stmts:
        for exc in stmts:
            for fin in stmts:
                method = template.format(
                    code['code'], exc['code'], fin['code'],
                    code['s'].format('code'),
                    exc['s'].format('exc'),
                    fin['s'].format('fin'))
                print(method)


def gen_py_test_cases_2e():
    stmts = [
        {'code': 'a', 's': '{} = 1'},
        {'code': 'r', 's': 'return "{}"'},
        {'code': 'e', 's': 'raise Exception("{}")'}
    ]
    template = '''    def test_py_exception_handling_permutation_{}{}(self):
        # given
        def x():
            try:
                {}
            except:
                {}
            return 0
        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("exc", str(cm.exception))
'''
    for code in stmts:
        for exc in stmts:
            method = template.format(
                code['code'], exc['code'],
                code['s'].format('code'),
                exc['s'].format('exc'))
            print(method)


def gen_py_test_cases_2f():
    stmts = [
        {'code': 'a', 's': '{} = 1'},
        {'code': 'r', 's': 'return "{}"'},
        {'code': 'e', 's': 'raise Exception("{}")'}
    ]
    template = '''    def test_py_exception_handling_permutation_{}{}(self):
        # given
        def x():
            try:
                {}
            finally:
                {}
            return 0
        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))
'''
    for code in stmts:
        for fin in stmts:
            method = template.format(
                code['code'], fin['code'],
                code['s'].format('code'),
                fin['s'].format('fin'))
            print(method)


def gen_w_test_cases_3():
    stmts = [
        {'code': 'r', 's': '"{}"'},
        {'code': 'e', 's': '(raise "{}")'}
    ]
    template = """    def test_w_exception_handling_permutation_{}{}{}(self):
        # when
        result = eval_str('''(try
                                {}
                             (except
                                {})
                             (finally
                                {}))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)
"""
    for code in stmts:
        for exc in stmts:
            for fin in stmts:
                method = template.format(
                    code['code'], exc['code'], fin['code'],
                    code['s'].format('code'),
                    exc['s'].format('exc'),
                    fin['s'].format('fin'))
                print(method)


def gen_w_test_cases_2e():
    stmts = [
        {'code': 'r', 's': '"{}"'},
        {'code': 'e', 's': '(raise "{}")'}
    ]
    template = \
        """    def test_w_exception_handling_permutation_exc_{}{}(self):
        # when
        result = eval_str('''(try
                                {}
                             (except
                                {}))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("exc", result.exception.message)
"""
    for code in stmts:
        for exc in stmts:
            method = template.format(
                code['code'], exc['code'],
                code['s'].format('code'),
                exc['s'].format('exc'))
            print(method)


def gen_w_test_cases_2f():
    stmts = [
        {'code': 'r', 's': '"{}"'},
        {'code': 'e', 's': '(raise "{}")'}
    ]
    template = \
        """    def test_w_exception_handling_permutation_fin_{}{}(self):
        # when
        result = eval_str('''(try
                                {}
                             (finally
                                {}))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)
"""
    for code in stmts:
        for fin in stmts:
            method = template.format(
                code['code'], fin['code'],
                code['s'].format('code'),
                fin['s'].format('fin'))
            print(method)


if __name__ == '__main__':
    gen_w_test_cases_2e()
    gen_w_test_cases_2f()
