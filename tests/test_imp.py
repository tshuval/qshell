# This should not be mounted
from time import time


# The class should also not be mounted
class C():
    pass


def imp_a():
    return "Woohoo"


def imp_b(a):
    return a


# A non-callable object also should not be mounted
not_callable = 1
