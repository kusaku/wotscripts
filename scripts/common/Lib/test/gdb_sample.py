# Embedded file name: scripts/common/Lib/test/gdb_sample.py


def foo(a, b, c):
    bar(a, b, c)


def bar(a, b, c):
    baz(a, b, c)


def baz(*args):
    print 42


foo(1, 2, 3)