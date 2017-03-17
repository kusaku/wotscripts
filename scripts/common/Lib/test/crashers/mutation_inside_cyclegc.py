# Embedded file name: scripts/common/Lib/test/crashers/mutation_inside_cyclegc.py
import weakref

class A(object):
    pass


def callback(x):
    del lst[:]


keepalive = []
for i in range(100):
    lst = [str(i)]
    a = A()
    a.cycle = a
    keepalive.append(weakref.ref(a, callback))
    del a
    while lst:
        keepalive.append(lst[:])