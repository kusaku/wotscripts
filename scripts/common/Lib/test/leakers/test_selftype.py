# Embedded file name: scripts/common/Lib/test/leakers/test_selftype.py
import gc

def leak():

    class T(type):
        pass

    class U(type):
        __metaclass__ = T

    U.__class__ = U
    del U
    gc.collect()
    gc.collect()
    gc.collect()