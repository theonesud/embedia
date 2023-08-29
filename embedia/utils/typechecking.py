from embedia.utils.exceptions import DefinitionError
import inspect


def check_type(var, type, func, src='input'):
    if not isinstance(var, type):
        raise TypeError(f"Func: {func.__qualname__} {src} expected type: {type}")


def check_values(var, values: list, var_name: str):
    if var not in values:
        raise ValueError(f"Var: {var_name} should be one of {values}, got: {var}")


def check_num_args(func, num_args: int, msg: str):
    sig = inspect.signature(func)
    if not len(sig.parameters) == num_args:
        raise DefinitionError(f"Func: {func.__qualname__} must have {num_args} argument(s) - {msg}")


def check_num_outputs(outputs, num: int, func, msg: str):
    if not len(outputs) == num:
        raise DefinitionError(f"Func: {func.__qualname__} must return {num} var(s) - {msg}")


def check_args(func, args: list):
    argspec = inspect.getfullargspec(func)
    arg_names = argspec.args
    if set(arg_names) != set(args):
        raise DefinitionError(f"{func.__qualname__} expects arguments: {set(args)},"
                              f" got: {set(arg_names)}")


def check_min_val(var, min_val: int, var_name: str):
    if var < min_val:
        raise ValueError(f"Var: {var_name} should be greater than or equal to {min_val}, got: {var}")


def check_not_false(var, var_name: str):
    if not var:
        raise ValueError(f"Var: {var_name} cant be empty, got: {var}")


def check_emb_input(input, func):
    if isinstance(input, str) or isinstance(input, list):
        if not input:
            raise ValueError(f"Var: EmbeddingModel __call__ input cant be empty, got: {input}")
    else:
        raise TypeError(f"Func: {func.__qualname__} input expected type: str / List[Any], got: {type(input)}")
