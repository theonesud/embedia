import inspect

from embedia.utils.exceptions import DefinitionError


def check_type(var, type, func, src="input"):
    if not isinstance(var, type):
        raise TypeError(f"Func: {func.__qualname__} {src} expected type: {type}")


def get_num_params(func):
    sig = inspect.signature(func)
    return len(sig.parameters)


def check_params(func, params: list):
    argspec = inspect.getfullargspec(func)
    param_names = argspec.args
    if set(param_names) != set(params):
        raise DefinitionError(
            f"{func.__qualname__} expects parameters: {sorted(set(params))},"
            f" got: {sorted(set(param_names))}"
        )


def check_min_val(var, min_val: int, var_name: str):
    if var < min_val:
        raise ValueError(
            f"Var: {var_name} should be greater than or equal to {min_val}, got: {var}"
        )


def check_exact_val(var, val: int, var_name: str):
    if var != val:
        raise ValueError(f"Var: {var_name} should be equal to {val}, got: {var}")
