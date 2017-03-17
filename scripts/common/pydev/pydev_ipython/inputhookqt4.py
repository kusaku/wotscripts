# Embedded file name: scripts/common/pydev/pydev_ipython/inputhookqt4.py
"""
Qt4's inputhook support function

Author: Christian Boos
"""
import os
import signal
import threading
from pydev_ipython.qt_for_kernel import QtCore, QtGui
from pydev_ipython.inputhook import allow_CTRL_C, ignore_CTRL_C, stdin_ready

class InteractiveShell:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_hook(self, *args, **kwargs):
        pass


got_kbdint = False
sigint_timer = None

def create_inputhook_qt4(mgr, app = None):
    """Create an input hook for running the Qt4 application event loop.
    
    Parameters
    ----------
    mgr : an InputHookManager
    
    app : Qt Application, optional.
        Running application to use.  If not given, we probe Qt for an
        existing application object, and create a new one if none is found.
    
    Returns
    -------
    A pair consisting of a Qt Application (either the one given or the
    one found or created) and a inputhook.
    
    Notes
    -----
    We use a custom input hook instead of PyQt4's default one, as it
    interacts better with the readline packages (issue #481).
    
    The inputhook function works in tandem with a 'pre_prompt_hook'
    which automatically restores the hook as an inputhook in case the
    latter has been temporarily disabled after having intercepted a
    KeyboardInterrupt.
    """
    if app is None:
        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtGui.QApplication([' '])
    ip = InteractiveShell.instance()
    if hasattr(ip, '_inputhook_qt4'):
        return (app, ip._inputhook_qt4)
    else:

        def inputhook_qt4():
            """PyOS_InputHook python hook for Qt4.
            
            Process pending Qt events and if there's no pending keyboard
            input, spend a short slice of time (50ms) running the Qt event
            loop.
            
            As a Python ctypes callback can't raise an exception, we catch
            the KeyboardInterrupt and temporarily deactivate the hook,
            which will let a *second* CTRL+C be processed normally and go
            back to a clean prompt line.
            """
            global sigint_timer
            global got_kbdint
            try:
                allow_CTRL_C()
                app = QtCore.QCoreApplication.instance()
                if not app:
                    return 0
                app.processEvents(QtCore.QEventLoop.AllEvents, 300)
                if not stdin_ready():
                    timer = QtCore.QTimer()
                    event_loop = QtCore.QEventLoop()
                    timer.timeout.connect(event_loop.quit)
                    while not stdin_ready():
                        timer.start(50)
                        event_loop.exec_()
                        timer.stop()

            except KeyboardInterrupt:
                ignore_CTRL_C()
                got_kbdint = True
                mgr.clear_inputhook()
                if os.name == 'posix':
                    pid = os.getpid()
                    if not sigint_timer:
                        sigint_timer = threading.Timer(0.01, os.kill, args=[pid, signal.SIGINT])
                        sigint_timer.start()
                else:
                    print '\nKeyboardInterrupt - Ctrl-C again for new prompt'
            except:
                ignore_CTRL_C()
                from traceback import print_exc
                print_exc()
                print 'Got exception from inputhook_qt4, unregistering.'
                mgr.clear_inputhook()
            finally:
                allow_CTRL_C()

            return 0

        def preprompthook_qt4(ishell):
            """'pre_prompt_hook' used to restore the Qt4 input hook
            
            (in case the latter was temporarily deactivated after a
            CTRL+C)
            """
            global sigint_timer
            global got_kbdint
            if sigint_timer:
                sigint_timer.cancel()
                sigint_timer = None
            if got_kbdint:
                mgr.set_inputhook(inputhook_qt4)
            got_kbdint = False
            return

        ip._inputhook_qt4 = inputhook_qt4
        ip.set_hook('pre_prompt_hook', preprompthook_qt4)
        return (app, inputhook_qt4)