def enforce_class_type(var, class_):
    try:
        if var is not None and not issubclass(var, class_):
            raise TypeError(f"{var} must be a subclass of {class_}")
    except TypeError:
        raise TypeError(f"{var} must be a subclass of {class_}")
