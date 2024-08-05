import inspect


def safe_call(func, *args, **kwargs):

    if is_wrapped(func):
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    parameters = sig.parameters.values()

    fn_args = {}

    for param in (param for param in parameters if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)):
        if param.name not in kwargs:
            raise ValueError(f"Unrecognized parameter: {param.name}")

        fn_args[param.name] = kwargs[param.name]

    func(**fn_args)


def is_wrapped(func) -> bool:
    return hasattr(func, "__wrapped__")


def get_context(kwargs):
    return get_from_context(kwargs, "context")


def get_from_context(kwargs, name: str):
    if name in kwargs:
        return kwargs[name]

    raise ValueError(f"No {name} provided")
