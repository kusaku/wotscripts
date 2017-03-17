# Embedded file name: scripts/common/pydev/pydev_ipython/inputhookpyglet.py
"""
Enable pyglet to be used interacive by setting PyOS_InputHook.

Authors
-------

* Nicolas P. Rougier
* Fernando Perez
"""
import os
import sys
from _pydev_imps import _pydev_time as time
from timeit import default_timer as clock
import pyglet
from pydev_ipython.inputhook import stdin_ready
if sys.platform.startswith('linux'):

    def flip(window):
        try:
            window.flip()
        except AttributeError:
            pass


else:

    def flip(window):
        window.flip()


def inputhook_pyglet():
    """Run the pyglet event loop by processing pending events only.
    
    This keeps processing pending events until stdin is ready.  After
    processing all pending events, a call to time.sleep is inserted.  This is
    needed, otherwise, CPU usage is at 100%.  This sleep time should be tuned
    though for best performance.
    """
    try:
        t = clock()
        while not stdin_ready():
            pyglet.clock.tick()
            for window in pyglet.app.windows:
                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                flip(window)

            used_time = clock() - t
            if used_time > 10.0:
                time.sleep(1.0)
            elif used_time > 0.1:
                time.sleep(0.05)
            else:
                time.sleep(0.001)

    except KeyboardInterrupt:
        pass

    return 0