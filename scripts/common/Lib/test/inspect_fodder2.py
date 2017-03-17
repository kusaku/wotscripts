# Embedded file name: scripts/common/Lib/test/inspect_fodder2.py


def wrap(foo = None):

    def wrapper(func):
        return func

    return wrapper


def replace(func):

    def insteadfunc():
        print 'hello'

    return insteadfunc


@wrap()
@wrap(wrap)
def wrapped():
    pass


@replace
def gone():
    pass


oll = lambda m: m
tll = lambda g: g and g and g
tlli = lambda d: d and d

def onelinefunc():
    pass


def manyargs(arg1, arg2, arg3, arg4):
    pass


def twolinefunc(m):
    return m and m


a = [None, lambda x: x, None]

def setfunc(func):
    globals()['anonymous'] = func


setfunc(lambda x, y: x * y)

def with_comment():
    world


multiline_sig = [lambda (x, y): x + y, None]

def func69():

    class cls70:

        def func71():
            pass

    return cls70


extra74 = 74

def func77():
    pass


extra78, stuff78 = 'xy'
extra79 = 'stop'

class cls82:

    def func83():
        pass


extra84, stuff84 = 'xy'
extra85 = 'stop'

def func88():
    return 90


def f():

    class X:

        def g():
            """doc"""
            return 42

    return X


method_in_dynamic_class = f().g.im_func