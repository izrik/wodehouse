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

    module['run_module_with_rt'] = WMagicFunction(run_module_with_rt, module,
                                                  check_args=False)
    module['run_file_with_rt'] = WMagicFunction(run_file_with_rt, module,
                                                check_args=False)
    module['run_source_with_rt'] = WMagicFunction(run_source_with_rt, module,
                                                  check_args=False)

    return module


def run_module_with_rt(rt, module, argv):
    return rt.run_module(module, argv)


def run_file_with_rt(rt, filename, argv):
    return rt.run_file(filename, argv)


def run_source_with_rt(rt, src, filename=None, argv=None):
    return rt.run_source(src, filename=filename, argv=argv)
