import sys


class QshellError(Exception):
    pass


class CommandNotFound(QshellError):
    pass


def log_err(err):
    sys.stderr.write('(error) ' + err + '\n')
