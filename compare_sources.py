#!/usr/bin/env python

from functions.exec_src import w_exec_src
from wtypes.function import WFunction
import functions.read
import functions.eval
from functions.scope import create_global_scope

with open('wodehouse.w') as f:
    src = f.read()

pyfuncs = {}

gs = create_global_scope()


def gather(module):
    for k, v in list(module.__dict__.items()):
        if hasattr(v, '__call__') and hasattr(v, '__doc__') and v.__doc__:
            src2 = v.__doc__
            # print(f'Reading docstring for {v} ... ', end='')
            ms = w_exec_src(src2, gs)
            for k2, v2 in ms.dict.items():
                if not isinstance(v2, WFunction):
                    continue
                pyfuncs[str(k2)] = v2
            # print('done.')


gather(functions.read)
gather(functions.eval)

ms = w_exec_src(src, enclosing_scope=gs)

for k, v in ms.dict.items():
    if not isinstance(v, WFunction):
        continue
    kk = str(k)
    if kk not in pyfuncs:
        print(f'compare_sources: {kk} NOT FOUND')
        continue
    if v.expr != pyfuncs[kk].expr:
        print(f'compare_sources: {kk} DOES NOT MATCH')
