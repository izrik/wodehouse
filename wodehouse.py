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
from functions.exception import format_stacktrace
from functions.exec_src import w_exec_src
from runtime import Runtime
from wtypes.list import WList
from wtypes.module import WModule
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


def repl(argv=None, primary_prompt=None, secondary_prompt=None):
    """(def repl ()
        (raise "Not implemented"))"""
    if primary_prompt is None:
        primary_prompt = '>>> '
    if secondary_prompt is None:
        secondary_prompt = '... '
    runtime = Runtime(argv)
    bm = runtime.builtins_module
    scope = WModule(builtins_module=bm, name='__main__', filename='__repl__')
    while True:
        try:
            prompt = primary_prompt
            buffer = ''

            while True:
                input_s = input(prompt)

                if input_s is None:
                    break

                input_s = buffer + input_s + '\n'

                if input_s.strip() == '':
                    break

                from functions.read import RanOutOfCharactersException
                from wtypes.stream import WStream
                from functions.read import parse
                from functions.read import read_whitespace_and_comments
                try:
                    stream = WStream(input_s)
                    parse(stream)
                    if stream.has_chars():
                        read_whitespace_and_comments(stream)
                        if stream.has_chars():
                            print('Warning: additional characters found at '
                                  'end of input expression.')
                except RanOutOfCharactersException:
                    buffer = input_s
                    prompt = secondary_prompt
                    continue
                break

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


def run_file(filename, argv=None):
    """(def run_file (filename argv)
        (let (src (read_file filename))
            (run_source src filename argv)))"""
    with open(filename) as f:
        src = f.read()
    return run_source(src, filename=filename, argv=argv)


def run_source(src, filename=None, argv=None):
    """(def run_source (src filename argv)
        (let (r (runtime argv))
            (let (rv (exec_src src (get_builtins_module r) "__main__"
                                filename))
                (if (isinstance rv 'Exception)
                    (let (stacktrace "TODO: format_stacktrace")
                        (exec
                            (print "Stacktrace (most recent call last):")
                            (print stacktrace)
                            (print
                                (format
                                    "Exception: {}"
                                    "TODO: get exception message from rv"))
                            "TODO: get exception from rv"))
                    rv))))"""
    runtime = Runtime(argv)
    rv = w_exec_src(src, builtins_module=runtime.builtins_module,
                    filename=filename, name='__main__')
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
        parser.add_argument('-v', '--verbose', action='store_true')
        args, remaining = parser.parse_known_args(argv)
        command = args.command
        argv = remaining

    if command:
        return run_source(command, filename='<string>', argv=argv)

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
