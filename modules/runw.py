from wtypes.magic_function import WMagicFunction
from wtypes.module import WModule


def create_runw_module(builtins_module, runtime):
    from wodehouse import run_module
    from wodehouse import run_file
    from wodehouse import run_source

    module = WModule(name='runw', builtins_module=builtins_module)
    module['run_module'] = WMagicFunction(run_module, module,
                                          check_args=False)
    module['run_file'] = WMagicFunction(run_file, module, check_args=False)
    module['run_source'] = WMagicFunction(run_source, module,
                                          check_args=False)

    return module