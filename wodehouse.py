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

from functions.eval import eval_str, is_exception
from functions.exception import format_stacktrace
from runtime import Runtime
from wtypes.list import WList
from wtypes.module import WModule
from wtypes.number import WNumber
from wtypes.string import WString
from version import __version__


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


def repl(runtime, primary_prompt=None, secondary_prompt=None):
    """(def repl ()
        (raise "Not implemented"))"""
    print(f'Wodehouse {__version__}')
    print('Copyright © 2014-2019 izrik')
    print(f'Type "quit" or "exit" to quit.')

    try:
        import readline  # noqa
    except ImportError:
        print('Warning: readline functionality not available')

    if primary_prompt is None:
        primary_prompt = '>>> '
    if secondary_prompt is None:
        secondary_prompt = '... '
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


def print_usage(argv):
    print(f'usage: {argv[0]} [option] ... '
          f'[-c cmd | -m mod | file | -] [arg] ...')
    print('Options and arguments:')
    print('-c cmd : program passed in as string (terminates option list)')
    print('-h     : print this help message and exit (also --help)')
    print('-m mod : run library module as a script (terminates option list)')
    print('-v     : verbose; can be supplied multiple times to increase')
    print('         verbosity')
    print('-V     : print the Wodehouse version number and exit '
          '(also --version)')
    print('file   : program read from script in file (terminates option '
          'list)')
    # TODO: determine if tty or not
    print('-      : program read from stdin (default)')\
        # 'interactive mode if a tty')
    print('arg ...: arguments passed to the program in sys.argv')


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

    command = None
    module = None
    filename = None
    verbose = 0
    i = 0
    while i < len(argv):
        # TODO: multiple short options in a single argv element
        if argv[i] == '-m':
            # TODO: print an error message if there's no argv[i+1]
            module = argv[i + 1]
            argv = argv[i + 1:]
            i += 1
            break
        if argv[i] == '-c':
            # TODO: print an error message if there's no argv[i+1]
            command = argv[i + 1]
            argv = argv[i + 1:]
            i += 1
            break
        if argv[i] == '-V':
            print(f'Wodehouse {__version__}')
            return
        if argv[i] in ['-h', '--help']:
            print_usage(argv)
            return
        if argv[i] == '--':
            break

        if argv[i] in ['-v', '--verbose']:
            verbose += 1

        if not argv[i].startswith('-'):
            filename = argv[i]
            break

        i += 1

    argv = argv[i:]
    runtime = Runtime(argv)

    if command:
        return runtime.run_source(command, filename='<string>', argv=argv)
    if module:
        return runtime.run_module(module, argv=argv)
    if filename is not None and filename != '-':
        return runtime.run_file(filename, argv=argv)
    return repl(runtime=runtime)


if __name__ == '__main__':
    main()
