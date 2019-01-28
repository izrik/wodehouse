# TODO: split tests up based on those that call the given units vs those that
# pass a string to eval_str. So a proper unit test would be:
#   `result = add(*Wlist(WNumber(1),WNumber(2),WNumber(3),WNumber(4)))`
# whereas an eval'd test would be:
#   `result = eval_str("(+ 1 2 3 4)", create_builtins_module())`
# Eventually, we want a set of tests that both the python code and the w-lang
# code can run.
