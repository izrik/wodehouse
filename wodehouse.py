#!/usr/bin/env python

"""
Wodehouse: An Object-oriented Functional Programming Language

(+ 1 2 3)
requires:
    integer literals
    '+' as a reference to a function
    function call

(print "Hello, world!")
requires:
    a `print` function
    function call
    a string type

(quote 1) --> 1
requires:
    quote symbol
    quote machinery in w_eval --> either macro or special code in w_eval

(quote (1)) --> (1)
requires
    quote a list
    proper list type, esp. comparing `WList` to python built-in `list`

'(1) --> (1)
requires
    syntax change: squote not allowed when delimiting strings, only dquote
    syntax change: read_expr("'(1)") --> WList(1)

"""

import sys
import traceback
from pathlib import Path

from functions.eval import eval_str
from functions.exec_src import w_exec_src
from functions.scope import create_global_scope, create_module_scope
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.string import WString


def repl_print(x):
    if isinstance(x, WNumber):
        print(x.value)
    elif isinstance(x, WString):
        print(str(x))
    elif isinstance(x, WList):
        print(str(x))
    else:
        print(x)
    return x


def iter_by_two(i):
    x = i.__iter__()
    while True:
        try:
            item1 = x.__next__()
        except StopIteration:
            break
        try:
            item2 = x.__next__()
        except StopIteration:
            raise Exception('Items are not in pairs')
        yield item1, item2


def repl(prompt=None):
    if prompt is None:
        prompt = '>>> '
    gs = create_global_scope()
    scope = create_module_scope(enclosing_scope=gs)
    while True:
        try:
            input_s = input(prompt)
            if input_s is None:
                continue
            if input_s.strip() in ['quit', 'exit']:
                break
            if input_s.strip() == '':
                continue
            value = eval_str(input_s, scope)
            repl_print(value)
        except EOFError:
            print('')
            break
        except KeyboardInterrupt:
            print('')
            continue
        except Exception as ex:
            print('Caught the following exception:')
            tb = traceback.format_exception(type(ex), ex, ex.__traceback__)
            for line in tb:
                print('  ' + line, end='')


def run_file(filename):
    with open(filename) as f:
        src = f.read()
    gs = create_global_scope()
    w_exec_src(src, enclosing_scope=gs, filename=filename)


def main():
    for arg in sys.argv[1:]:
        path = Path(arg)
        if path.is_file():
            run_file(arg)
        elif path.is_dir():
            for f in path.glob('*'):
                if f.is_file():
                    run_file(f)
    if len(sys.argv) < 2:
        repl()


if __name__ == '__main__':
    main()
