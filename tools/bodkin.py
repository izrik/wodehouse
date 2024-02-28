#!/usr/bin/env python3

import ast
from pprint import pprint
from typing import Sequence

from macros.def_ import Def
from macros.if_ import If
from macros.import_ import Import
from macros.let import Let
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.string import WString
from wtypes.symbol import WSymbol


def translate_py2w(source: str) -> str:
    tree = ast.parse(source, type_comments=True)
    forms = convert_py2w(tree)
    return str(forms)


def convert_py2w(node) -> WObject:
    if isinstance(node, ast.Module):
        values = []
        for body_item in node.body:
            values.append(convert_py2w(body_item))
        return WList(*values)
    if isinstance(node, ast.Import):
        statements = []
        for alias in node.names:
            if alias.asname:
                # w = WList(Import(), WSymbol(alias.name),
                # WSymbol(alias.asname))
                raise NotImplementedError
            else:
                w = WList(Import(), WSymbol(alias.name))
            statements.append(w)
        return WList(*statements)
    if isinstance(node, ast.ImportFrom):
        statements = []
        for alias in node.names:
            if alias.asname:
                # w = WList(Import(), WSymbol(alias.name),
                # WSymbol(alias.asname))
                raise NotImplementedError
            else:
                w = WList(Import(), WSymbol(node.module), WSymbol(alias.name))
            statements.append(w)
        return WList(*statements)
    if isinstance(node, ast.FunctionDef):
        statements = [convert_py2w(stmt) for stmt in node.body]
        return WList(
            Def(),
            WSymbol(node.name),
            WList(*node.args.args),
            *statements)
    if isinstance(node, ast.Assign):
        return WList(
            Let(),
            WList(convert_py2w(node.targets[0]),
                  convert_py2w(node.value))
        )
    if isinstance(node, ast.Name):
        return WSymbol(node.id)
    if isinstance(node, ast.Call):
        return WList(
            convert_py2w(node.func),
            *[convert_py2w(arg) for arg in node.args]
        )
    if isinstance(node, ast.Attribute):
        return []
    if isinstance(node, ast.Expr):
        return convert_py2w(node.value)
    if isinstance(node, ast.Return):
        return convert_py2w(node.value)
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, int):
            return WNumber(value)
        if isinstance(value, str):
            return WString(value)
        raise NotImplementedError(f'Unknown value "{value}"')
    if isinstance(node, ast.If):
        if node.orelse:
            return WList(
                If(),
                convert_py2w(node.test),
                *[convert_py2w(stmt) for stmt in node.body],
                *[convert_py2w(stmt) for stmt in node.orelse])
        return WList(
            If(),
            convert_py2w(node.test),
            *[convert_py2w(stmt) for stmt in node.body])
    if isinstance(node, ast.List):
        elts = []
        for elt in node.elts:
            elts.append(convert_py2w(elt))
        return WList(
            WSymbol.get('quote'),
            *elts)
    if isinstance(node, ast.For):
        pass
    if isinstance(node, ast.Try):
        if len(node.handlers) > 1:
            raise NotImplementedError(
                'Can\'t do more than one exception handler, '
                f'node "{node}" ({node.lineno},{node.col_offset})')

        ts = [WSymbol.get('try')]

        body_statements = [convert_py2w(_) for _ in node.body]
        if len(body_statements) > 1:
            ts.append(WList(WSymbol.get('exec'), *body_statements))
        else:
            ts.append(body_statements[0])

        handlers = []
        for h in node.handlers:
            pieces = [WSymbol.get('except')]
            if h.type:
                pieces.append(WSymbol.get(h.type.id))
            if h.name:
                pieces.append(WSymbol.get('as'))
                pieces.append(WSymbol.get(h.name))
            if len(h.body) > 1:
                bs = [convert_py2w(_) for _ in h.body]
                pieces.append(
                    WList(WSymbol.get('exec'), *bs))
            else:
                pieces.append(convert_py2w(h.body[0]))
            wh = WList(*pieces)
            handlers.append(wh)
            ts.append(wh)

        if node.finalbody:
            fbs = []
            for fb in node.finalbody:
                fbs.append(convert_py2w(fb))
            if len(node.finalbody) > 1:
                fw = WList(WSymbol.get('exec'), *fbs)
            else:
                fw = fbs[0]
            ts.append(WList(WSymbol.get('finally'), fw))

        return WList(*ts)
    if isinstance(node, ast.Raise):
        # TODO: type
        # TODO: exception message
        return WSymbol.get('raise')
    raise NotImplementedError(
        f'AST node type "{node}" ({node.lineno},{node.col_offset})')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('direction', choices=['py2w', 'w2py'])
    parser.add_argument('filename')
    args = parser.parse_args()
    filename = args.filename
    if args.direction == 'py2w':
        with open(filename) as f:
            py_contents = f.read()
        w_contents = translate_py2w(py_contents)
        from wodehouse import repl_print

        for _ in w_contents:
            repl_print(_)
    else:
        with open(filename) as f:
            py_contents = f.read()
        w_contents = translate_w2py(py_contents)
        print(w_contents)
