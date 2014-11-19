import sys
from qshell.core import ctx


# Decorator for registering functions as commands
def command(func):
    if callable(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        ctx.register(func.__name__, func)
        return inner
    else:
        def decorator(fn):
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            ctx.register(func, fn)
            return inner
        return decorator


# Decorator for init function. Run immediately
def init(func):
    def inner():
        args, kwargs = ctx._parse_args(' '.join(sys.argv[1:]))
        return func(*args, **kwargs)
    return inner()
