# Embedded file name: scripts/common/pydev/_pydev_bundle/pydev_is_thread_alive.py
from _pydev_imps import _pydev_threading as threading
_temp = threading.Thread()
if hasattr(_temp, '_is_stopped'):

    def is_thread_alive(t):
        try:
            return not t._is_stopped
        except:
            return t.isAlive()


elif hasattr(_temp, '_Thread__stopped'):

    def is_thread_alive(t):
        try:
            return not t._Thread__stopped
        except:
            return t.isAlive()


else:

    def is_thread_alive(t):
        return t.isAlive()


del _temp