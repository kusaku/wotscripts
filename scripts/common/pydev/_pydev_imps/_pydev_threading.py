# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_threading.py
from threading import *
from threading import enumerate, currentThread, Condition, Event, Thread, Lock
try:
    from threading import settrace
except:
    pass

try:
    from threading import Timer
except:
    pass

try:
    from gevent import monkey
    saved = monkey.saved['threading']
    for key, val in saved.items():
        globals()[key] = val

except:
    pass