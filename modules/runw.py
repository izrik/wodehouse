from wtypes.magic_function import WMagicFunction
from wtypes.module import WModule


def create_runw_module(builtins_module, runtime):
    module = WModule(name='runw', builtins_module=builtins_module)
    module['run_module'] = WMagicFunction(runtime.run_module, module,
                                          check_args=False)
    module['run_file'] = WMagicFunction(runtime.run_file, module,
                                        check_args=False)
    module['run_source'] = WMagicFunction(runtime.run_source, module,
                                          check_args=False)

    return module
