# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_thread.py
try:
    from thread import *
except:
    from _thread import *

try:
    from gevent import monkey
    saved = monkey.saved['thread']
    for key, val in saved.items():
        globals()[key] = val

except:
    pass