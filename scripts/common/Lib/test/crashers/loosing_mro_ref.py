# Embedded file name: scripts/common/Lib/test/crashers/loosing_mro_ref.py
"""
There is a way to put keys of any type in a type's dictionary.
I think this allows various kinds of crashes, but so far I have only
found a convoluted attack of _PyType_Lookup(), which uses the mro of the
type without holding a strong reference to it.  Probably works with
super.__getattribute__() too, which uses the same kind of code.
"""

class MyKey(object):

    def __hash__(self):
        return hash('mykey')

    def __cmp__(self, other):
        X.__bases__ = (Base2,)
        z = []
        for i in range(1000):
            z.append((i, None, None))

        return -1


class Base(object):
    mykey = 'from Base'


class Base2(object):
    mykey = 'from Base2'


X = type('X', (Base,), {MyKey(): 5})
print X.mykey