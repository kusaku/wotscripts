# Embedded file name: scripts/common/pydev/pydev_ipython/inputhooktk.py
from pydev_ipython.inputhook import stdin_ready
TCL_DONT_WAIT = 2

def create_inputhook_tk(app):

    def inputhook_tk():
        while app.dooneevent(TCL_DONT_WAIT) == 1:
            if stdin_ready():
                break

        return 0

    return inputhook_tk