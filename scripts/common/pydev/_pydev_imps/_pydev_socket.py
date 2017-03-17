# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_socket.py
from socket import *
try:
    from gevent import monkey
    saved = monkey.saved['socket']
    for key, val in saved.items():
        globals()[key] = val

except:
    pass