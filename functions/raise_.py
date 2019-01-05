from functions.str import w_str


def w_raise(description):
    raise Exception(w_str(description).value)
