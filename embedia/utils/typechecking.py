from embedia.utils.exceptions import DefinitionError
import inspect


def check_type(var, type):
    if not isinstance(var, type):
        raise DefinitionError(f"Expected type: {type}, got: {type(var)}")


def check_num_args(func, num_args, args):
    sig = inspect.signature(func)
    if not len(sig.parameters) == num_args:
        raise DefinitionError(f"{func} must have {num_args} argument(s)")


def check_min_val(name, var, min_val):
    if var < min_val:
        raise DefinitionError(f"{name} should be greater than or equal to {min_val}. Got: {var}")
