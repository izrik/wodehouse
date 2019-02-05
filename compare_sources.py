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


def gather(module):
    for k, v in list(module.__dict__.items()):
        if hasattr(v, '__call__') and hasattr(v, '__doc__') and \
                v.__doc__ and v.__module__ == module.__name__:
            src2 = v.__doc__
            # print(f'Reading docstring for {v} ... ', end='')
            _ms = w_exec_src(src2, builtins_module=bm)
            for k2, v2 in _ms.dict.items():
                if not isinstance(v2, WFunction):
                    continue
                pyfuncs[str(k2)] = v2
            # print('done.')


gather(functions.read)
gather(functions.eval)
gather(wodehouse)

ms = w_exec_src(src, builtins_module=bm)

problem = False
for k, v in ms.dict.items():
    if not isinstance(v, WFunction):
        continue
    if v.enclosing_scope is not ms:
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
