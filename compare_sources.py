#!/usr/bin/env python
import sys

from functions.exec_src import w_exec_src
from wtypes.function import WFunction
import functions.read
import functions.eval
import wodehouse

with open('wodehouse.w') as f:
    src = f.read()

pyfuncs = {}

runtime = wodehouse.Runtime(sys.argv[:1])
bm = runtime.builtins_module

logging_enabled = False


def log(msg):
    if logging_enabled:
        print(msg)


def gather(module, module_name=None):
    if module_name is None:
        module_name = module.__name__
    log(f'gathering from {module}, __name__ == {module_name}')
    for k, v in list(module.__dict__.items()):
        log(f'  considering {k}, __module__ == {v.__module__ if hasattr(v, "__module__") else "<missing>"}')
        if hasattr(v, '__call__') and hasattr(v, '__doc__') and \
                v.__doc__ and v.__module__ == module_name:
            src2 = v.__doc__
            # log(f'Reading docstring for {v} ... ', end='')
            _ms = w_exec_src(src2, builtins_module=bm)
            for k2, v2 in _ms.dict.items():
                log(f'  considering for pyfunc {k2}')
                if not isinstance(v2, WFunction):
                    continue
                log(f'  adding pyfunc {k2}')
                pyfuncs[str(k2)] = v2
            # log('done.')


gather(functions.read)
gather(functions.eval)
gather(wodehouse)

log('pyfuncs:')
for k, v in pyfuncs.items():
    log(f'  {k}: {v}')
log('')

ms = w_exec_src(src, builtins_module=bm)

problem = False
for k, v in ms.dict.items():
    if not isinstance(v, WFunction):
        continue
    if v.enclosing_scope is not ms:
        log(f'{v} is not enclosed by {ms}')
        continue
    kk = str(k)
    if kk not in pyfuncs:
        print(f'compare_sources: {kk} NOT FOUND')
        problem = True
        continue
    if v.expr != pyfuncs[kk].expr:
        print(f'compare_sources: {kk} DOES NOT MATCH')
        problem = True
if not problem:
    print('compare_sources: Everything matches.')
