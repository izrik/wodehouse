from runtime import Runtime
from wtypes.magic_function import WMagicFunction


def w_runtime(argv):
    return Runtime(argv)


class GetCurrentRuntime(WMagicFunction):
    def __init__(self, runtime, enclosing_scope):
        super().__init__(self.get_current_runtime, enclosing_scope)
        self.runtime = runtime

    def get_current_runtime(self):
        return self.runtime


def add_emit_listener(runtime, listener, enclosing_scope):
    return runtime.add_emit_listener(listener, enclosing_scope)


def remove_emit_listener(runtime, listener):
    return runtime.remove_emit_listener(listener)
