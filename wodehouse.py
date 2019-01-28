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
import argparse
import sys

import traceback

from functions.eval import eval_str, is_exception
from functions.exec_src import w_exec_src
from functions.scope import create_module_scope
from runtime import Runtime
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


def repl(prompt=None, argv=None):
    """(def repl ()
        (raise "Not implemented"))"""
    if prompt is None:
        prompt = '>>> '
    runtime = Runtime(argv)
    bm = runtime.builtins_module
    scope = create_module_scope(builtins_module=bm, name='__main__',
                                filename='__repl__')
    while True:
        try:
            input_s = input(prompt)
            if input_s is None:
                continue
            if input_s.strip() in ['quit', 'exit']:
                break
            if input_s.strip() == '':
                continue
            rv = eval_str(input_s, scope)
            if is_exception(rv):
                stacktrace = format_stacktrace(rv.stack,
                                               default_filename='<stdin>')
                print('Stacktrace (most recent call last):')
                print(stacktrace)
                print(f'Exception: {rv.exception.message.value}')
            else:
                repl_print(rv)
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


def format_stacktrace(stack, default_filename=None):
    if default_filename is None:
        default_filename = '<unknown>'
    frames = []
    while stack is not None:
        expr = stack.expanded_expr
        if not expr:
            expr = stack.expr
        if not expr:
            stack = stack.prev
            continue
        pos = expr.position
        filename = pos.filename or default_filename
        line = pos.line or '<unknown>'
        expansion = pos.get_source_line().strip()
        if len(expansion) > 64:
            expansion = expansion[0:60] + ' ...'
        frames.append(
            f'  File "{filename}", line {line}, in '
            f'{stack.get_location()}\n'
            f'    {expansion}')
        stack = stack.prev
    frames.reverse()
    return '\n'.join(frames)


def run_file(filename, argv=None):
    """(def run_file (filename argv)
        (raise "Not implemented"))"""
    with open(filename) as f:
        src = f.read()
    return run_source(src, filename=filename, argv=argv)


def run_source(src, filename=None, argv=None):
    """(def run_source (src filename argv)
        (raise "Not implemented"))"""
    runtime = Runtime(argv)
    rv = w_exec_src(src, builtins_module=runtime.builtins_module,
                    filename=filename)
    if is_exception(rv):
        stacktrace = format_stacktrace(rv.stack)
        print('Stacktrace (most recent call last):')
        print(stacktrace)
        print(f'Exception: {rv.exception.message.value}')
        return rv.exception
    return rv


def main():
    """(def main ()
    (let (parsed (parse_args
                    '(
                        (verbose ("-v" "--verbose") 0)
                        (command ("-c" "--command") 1)
                        #(run_files ("--run_files") 'n)
                     )
                     argv))
         (let (argv (get parsed '__remaining_argv__))
             (if (in 'command parsed)
                (run_source (get parsed 'command) "<string>" argv)
                (if (or (>= 0 (len argv)) (eq (car argv) "-"))
                    (print 'repl)
                    (run_file (car argv) (cdr argv)))))))"""
    argv = []
    if len(sys.argv) > 1:
        argv = sys.argv[1:]

    args = None
    command = None
    if len(argv) > 0 and argv[0] and argv[0].startswith('-'):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--command',
                            help='program passed in as string')
        parser.add_argument('--run-files', nargs='+')
        parser.add_argument('-v', '--verbose', action='store_true')
        args, remaining = parser.parse_known_args(argv)
        command = args.command
        argv = remaining

    if command:
        return run_source(command, filename='<string>', argv=argv)

    if args and args.run_files:
        rv = None
        files_to_run = []
        for filename in args.run_files:
            from pathlib import Path
            path = Path(filename)
            if not path.exists():
                raise FileNotFoundError(f'Could not find file "{filename}".')

            def add_file_or_dir(_path):
                f = str(_path)
                if _path.is_file() and f.endswith('.w'):
                    files_to_run.append(f)
                elif _path.is_dir():
                    for f in _path.glob('*'):
                        add_file_or_dir(f)

            add_file_or_dir(path)

        for file_to_run in files_to_run:
            if args.verbose:
                print(f'Running file {file_to_run} ... ', end='')
            rv = run_file(file_to_run, argv=argv)
            if args.verbose:
                print('done.')
        return rv

    filename = None
    if len(argv) > 0:
        if argv[0] != '-' and argv[0].startswith('-'):
            print(f'Unknown option: {argv[0]}')
            return
        filename = argv[0]

    if filename is not None and filename != '-':
        return run_file(filename, argv=argv)

    repl(argv=argv)


if __name__ == '__main__':
    main()
