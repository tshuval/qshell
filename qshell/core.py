import os
import sys
import shlex
import inspect
import traceback
from cmd import Cmd
from functools import partial
from qshell.exceptions import CommandNotFound, log_err


class _Cmd(Cmd):
    """
    Subclass of Cmd.
    Passes 'do_*' methods to the Context instance for execution.
    Overrides some Cmd methods to support the Context idea.
    """
    def __init__(self, context, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self._context = context

    def __getattr__(self, name):
        """Pass 'do_' commands to the Context instance"""
        if name.startswith('do_'):
            try:
                return self._context.get_command_wrapper(name[3:].lower())
            except CommandNotFound:
                log_err('Unknown command: %s' % name[3:])
        return getattr(Cmd, name)

    def completenames(self, text, *ignored):
        """Override for autocompleting from the context"""
        text = text.lower()
        return filter(lambda u: u.startswith(text), self._context.get_names())

    def do_help(self, arg):
        """Display a command's help text"""
        if arg:
            try:
                cmd = self._context.get_command(arg.lower())
            except CommandNotFound:
                log_err('Unknown command: %s' % arg)
            else:
                sys.stdout.write('(help) %r\n' % cmd)
        else:
            sys.stdout.write(
                "(help) Available commands (type 'help <command>'):\n")
            sys.stdout.write('  '.join(sorted(self._context.get_names())))
            sys.stdout.write('\n')

    def default(self, line):
        """Do nothing"""
        pass

    def emptyline(self):
        """Do nothing"""
        pass


class Command(object):
    """Represents a single command"""
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.help = inspect.getdoc(func) or ''
        self.arg_string = self._inspect_func(func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        s = 'Syntax: %s %s \n%s' % (self.name, self.arg_string, self.help)
        return s.strip()

    def _inspect_func(self, func):
        """Prepare a visualization of the command arguments"""
        ins = inspect.getargspec(func)
        line = []
        if ins.keywords:
            line.append('[**%s]' % ins.keywords)
        if ins.varargs:
            line.append('[*%s]' % ins.varargs)
        for default in reversed(ins.defaults or ()):
            arg = ins.args.pop()
            line.append('[%s=%s]' % (arg, default))
        line.extend(reversed(ins.args))

        return ' '.join(reversed(line))


class Context(object):
    """
    The main context. A regsitry of commands.
    Serves as a proxy between the Cmd class to the actual commands (functions).
    """
    def __init__(self, prompt='>>> '):
        self._registry = {}
        self.cmd = _Cmd(self)

    def register(self, name, func):
        name = name.lower().rstrip('_')
        self._registry[name] = Command(name, func)

    def start_loop(self, intro=''):
        try:
            self.cmd.cmdloop(intro)
        except KeyboardInterrupt:
            sys.stdout.write('\nBye\n')

    def get_names(self):
        return self._registry.keys()

    def get_command(self, name):
        """Returns the Command instance representing 'name' command"""
        try:
            return self._registry[name]
        except KeyError:
            raise CommandNotFound(name)

    def get_command_wrapper(self, name):
        """
        Returns a execute_command() 'partial' callable, referring the
        command to be executed as received in `name`.
        If not found, will raise CommandNotFound.
        """
        self.get_command(name)
        return partial(self.execute_command, name)

    def execute_command(self, name, line):
        """
        Called by the _Cmd class with the following arguments:
        `name` - name of the command to execute.
        `line` - a single string of args received from the Cmd super class.
        """
        cmd = self._registry[name]
        args, kwargs = self._parse_args(line)
        try:
            try:
                result = cmd(*args, **kwargs)
                sys.stdout.write('%s\n' % (str(result) or '(ok)'))
            except TypeError as e:
                # In case of TypeError, we need to check if it was due to
                # bad call to the command function, or in the function itself.
                exc_info = sys.exc_info()
                if (os.path.dirname(__file__) ==
                        os.path.dirname(
                            traceback.extract_tb(exc_info[2])[-1][0])):
                    # Bad arguments in the call to the command function
                    s = str(e).split('()', 1)
                    s = s[len(s)-1].strip()
                    log_err("Bad arguments: '%s' %s" % (name, s))
                else:
                    # TypeError raised inside the command function, so re-raise
                    # This will be catched by the below 'except' block
                    raise exc_info[0], exc_info[1], exc_info[2]
        except Exception as e:
            # Command execution throws an exception
            log_err("Exception in '%s':\n%s" % (name, traceback.format_exc()))

    def _parse_args(self, line):
        """
        Parses the arguments from a string 'line'.
        Turns args like "name=john" into {'name': 'john'}.
        Also, identify ints/floats and cast as needed.
        """
        args = []
        kwargs = {}
        arg_list = shlex.split(line)
        while arg_list:
            arg = arg_list.pop(0)
            if '=' in arg:
                k, v = arg.split('=', 1)
                kwargs[k] = self._cast(v)
            else:
                args.append(self._cast(arg))

        return args, kwargs

    def _cast(self, v):
        # Cast int/float
        try:
            fv = float(v)
        except ValueError:
            return v
        if not '.' in v:
            fv = int(fv)
        return fv

    @property
    def prompt(self):
        return self.cmd.prompt

    @prompt.setter
    def prompt(self, value):
        self.cmd.prompt = value

# A global registry context
ctx = Context()
