import qshell


@qshell.command
def echo(something, n=1):
    """Echo 'something' back"""
    return something * n


@qshell.command
def test(x, y=0, *args, **kwargs):
    return "Hello World", x, y


@qshell.command
def get_():
    """When executed, should raise a TypeError referring the 'f(1)' line"""
    def f():
        pass
    f(1)


@qshell.init
def connect(username=None, password=None):
    qshell.session.conn = {'username': username, 'password': password}


qshell.imp('tests.test_imp')


if __name__ == '__main__':
    qshell.start_loop()
