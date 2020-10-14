import unittest
from unittest.mock import patch

from wodehouse import print_usage


class PrintUsageTest(unittest.TestCase):
    @patch('wodehouse.print')
    def test_print_usage(self, _print):
        # when
        result = print_usage(['program'])
        # then
        self.assertIsNone(result)
        # and
        _print.call_args_list == [
            ('usage: program [option] ... '
             '[-c cmd | -m mod | file | -] [arg] ...',),
            ('Options and arguments:',),
            ('-c cmd : program passed in as string '
             '(terminates option list,)',),
            ('-h     : print this help message and exit (also --help,)',),
            ('-m mod : run library module as a script '
             '(terminates option list,)',),
            ('-v     : verbose; can be supplied multiple times to increase',),
            ('         verbosity',),
            ('-V     : print the Wodehouse version number and exit '
             '(also --version,)',),
            ('file   : program read from script in file (terminates option '
             'list,)',),
            ('-      : program read from stdin (default,)',),
            ('arg ...: arguments passed to the program in sys.argv',),
        ]
