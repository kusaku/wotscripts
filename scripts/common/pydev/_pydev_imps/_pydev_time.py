# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_time.py
from time import *
try:
    from gevent import monkey
    saved = monkey.saved['time']
    for key, val in saved.items():
        globals()[key] = val

except:
    pass