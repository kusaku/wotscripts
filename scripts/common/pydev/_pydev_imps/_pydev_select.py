# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_select.py
from select import *
try:
    from gevent import monkey
    saved = monkey.saved['select']
    for key, val in saved.items():
        globals()[key] = val

except:
    pass