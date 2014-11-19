import inspect
import importlib
from qshell.session import session
from qshell.core import ctx, log_err


def start_loop(prompt='>>> ', intro=''):
    """Starts the shell"""
    session.start()
    ctx.prompt = prompt
    ctx.start_loop(intro)


def imp(name):
    """
    Imports all commands from module 'name'.
    The commands to be imported are determined in the following order:
    1. __commands__, or
    2. __all__, or
    3. all functions defined in the module.
    """
    try:
        module = importlib.import_module(name)
    except ImportError:
        log_err('Unable to import module %s\n' % name)
        return

    # Get the names of commands
    commands = (getattr(module, '__commands__', None) or
                getattr(module, '__all__', None))
    if not commands:
        commands = [attr for attr in dir(module) if not attr.startswith('_')]
        direct = True
    else:
        direct = False

    # Get the objects
    commands = [getattr(module, cmd) for cmd in commands]

    # Filter functions only
    commands = filter(lambda fn: inspect.isfunction(fn), commands)

    # If commands were imported directly (using dir(module)), ignore functions
    # that might be imported from other modules.
    if direct:
        commands = filter(lambda fn: fn.__module__ == name, commands)

    # Register the commands
    [ctx.register(fn.__name__, fn) for fn in commands]
