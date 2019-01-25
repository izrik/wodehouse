#!/usr/bin/env python
import sys

import macros.import_
from functions.exec_src import w_exec_src
from modules.sys import create_sys_module
from wtypes.function import WFunction
import functions.read
import functions.eval
from functions.scope import create_global_scope
from wtypes.symbol import WSymbol

with open('wodehouse.w') as f:
    src = f.read()

pyfuncs = {}

gs = create_global_scope()


def gather(module):
    for k, v in list(module.__dict__.items()):
        if hasattr(v, '__call__') and hasattr(v, '__doc__') and \
                v.__doc__ and v.__module__ == module.__name__:
            src2 = v.__doc__
            # print(f'Reading docstring for {v} ... ', end='')
            _ms = w_exec_src(src2, global_scope=gs)
            for k2, v2 in _ms.dict.items():
                if not isinstance(v2, WFunction):
                    continue
                pyfuncs[str(k2)] = v2
            # print('done.')


gather(functions.read)
gather(functions.eval)

w_sys = create_sys_module(gs, argv=sys.argv[:1])
macros.import_._global_import_cache[WSymbol.get('sys')] = w_sys
ms = w_exec_src(src, global_scope=gs)

for k, v in ms.dict.items():
    if not isinstance(v, WFunction):
        continue
    kk = str(k)
    if kk not in pyfuncs:
        print(f'compare_sources: {kk} NOT FOUND')
        continue
    if v.expr != pyfuncs[kk].expr:
        print(f'compare_sources: {kk} DOES NOT MATCH')
