from runtime import Runtime
from wtypes.magic_function import WMagicFunction


def w_runtime(argv):
    return Runtime(argv)


def add_emit_listener(runtime, listener, enclosing_scope):
    return runtime.add_emit_listener(listener, enclosing_scope)


def remove_emit_listener(runtime, listener):
    return runtime.remove_emit_listener(listener)
