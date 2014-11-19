# Introduction

`qshell` (**q** stands for **quick**) provides a fast and easy way for creating shell interface (CLI) for your Python project.

## Features
* Transform existing *functions* into CLI *commands* by adding a decorator.
* Shell support for history, command completion and help.
* Intelligent parsing of command line arguments.
* Thread-safe session environment.
* Transform a whole module into an API shell with one line of code!

# Installation
Setting up a shell for your API is very fast and easy. Install the `qshell` package:

    $ pip install qshell

# Quickstart
We will define a simple function that echoes back its input, and transform it into a shell command:

    from qshell import command, start_loop

    @command
    def echo(something):
        """Echo 'something' back"""
        return something

    start_loop()

**Congratulations!** You have just written yout first command-line interface (CLI) which implements the `echo` command!

Save the code in a file (e.g. `my_first_api.py`) and run it from the command line:

    $ python my_first_api.py

This will start the shel and you'll see the `>>>` prompt.

Let's test our command:

    >>> echo "Hello world!"
    Hello world!
    >>> _

### Optional arguments

`qshell` commands support optional arguments. Let's modify our code:

    @command
    def echo(something, n=1):
        """Echo 'something' back 'n' times"""
        return something * n

Again, save the file and run it. Now let's test our modified command:

    >>> echo xo
    xo
    >>> echo xo n=3
    xoxoxo
    >>> _

Note how `n` was passed to the function as type `int`. Numeric arguments of types `int` and `float` will be cast to the apporpriate type before being passed to the function.

### Getting help inside the shell
To get a list of available commands, type `help` or `?`:

    >>> ?
    (help) Available commands (type 'help <command>'):
    echo
    >>> _

To get help for a specific command, type `help` or `?` and the command name:

    >>> ? echo
    (help) Syntax: echo something [n=1]
    Echo 'something' back 'n' times
    >>> _

As you can see, `qshell` displays the function's arguments and docstring as help.

## Loading a module with `qshell.imp()`
You have an existing Python module with lots of functions that you want to use in your CLI. It might be easier to tell `qshell` to import and load the entire module, instead of decorating every function with the `@command` decorator.

`qshell` has a special method of doing so:

    import qshell

    qshell.imp('my_package.my_module')
    qshell.start_loop()

This will load your functions from `my_package.my_module` and start the shell.  *(Hint: type `?` at the prompt to see them!)*

##### <a name="loading-with-imp"></a>How `qshell` determines which functions to load?
`qshell` will try to load functions by looking for a list or tuple containing their names, in the following order:

1. If `__commands__` is defined in the module, use it. Else...
2. If `__all__` is defined, use it. Else...
3. Import all functions defined in the module.

# API
Below is a list of objects available from the `qshell` package.

## Decorators
**command(** *[name]* **)**

Registers a function as a command.
By default, the command name will be the function name, lower-cased. To override this behavior, pass *name* to the decorator and it will be used instead.

  Examples:

    @command
    def go():
        """Assign the function to a command 'go'"""
        pass

    @command('bar')
    def foo():
        """Assign the function to a command 'bar'"""
        pass

    @command
    def set_():
        """
        Reserved keywords are supported. Simply append '_' to the function name.
        In this example, the function will be assigned to a command 'set'.
        """
        pass

**init()**

Defines a function to be run immediately at startup. The command-line arguments (from `sys.argv`) will be passed to the function.

  Example:

    @init
    def connect(user=None, password=None):
        pass

## Functions
**start_loop(** *[prompt='>>> '][, intro='']* **)**

Starts the command line loop (the shell). Use *prompt* as the command-line prompt. Display an *intro* message at start.

**imp(** *module_name* **)**

Imports all functions from module *module_name* and registers them as commands. Click [here](#loading-with-imp) for explanation on how `qshell` determines what to import.

## Variables
**session**

A thread-local storage object. You can use it to share data across functions/commands.

**ctx**

The main (global) context instance. You would normally won't need to access it directly. See inline documentation for more information.
