import inspect

from embedia.utils.exceptions import DefinitionError


def check_type(var, type, func, src='input'):
    if not isinstance(var, type):
        raise TypeError(f"Func: {func.__qualname__} {src} expected type: {type}")


def get_num_args(func):
    sig = inspect.signature(func)
    return len(sig.parameters)


def check_args(func, args: list):
    argspec = inspect.getfullargspec(func)
    arg_names = argspec.args
    if set(arg_names) != set(args):
        raise DefinitionError(f"{func.__qualname__} expects arguments: {sorted(set(args))},"
                              f" got: {sorted(set(arg_names))}")


def check_min_val(var, min_val: int, var_name: str):
    if var < min_val:
        raise ValueError(f"Var: {var_name} should be greater than or equal to {min_val}, got: {var}")
