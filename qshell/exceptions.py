import sys


class qshellError(Exception):
    pass


class CommandNotFound(qshellError):
    pass


def log_err(err):
    sys.stderr.write('(error) ' + err + '\n')
