# Embedded file name: scripts/common/pydev/_pydev_bundle/pydev_monkey_qt.py
from __future__ import nested_scopes

def set_trace_in_qt():
    from _pydevd_bundle import pydevd_tracing
    from _pydevd_bundle.pydevd_comm import get_global_debugger
    debugger = get_global_debugger()
    if debugger is not None:
        pydevd_tracing.SetTrace(debugger.trace_dispatch)
    return


_patched_qt = False

def patch_qt():
    """
    This method patches qt (PySide, PyQt4, PyQt5) so that we have hooks to set the tracing for QThread.
    """
    global _patched_qt
    if _patched_qt:
        return
    else:
        _patched_qt = True
        patch_qt_on_import = None
        try:
            import PySide
        except:
            try:
                import PyQt4
                patch_qt_on_import = 'PyQt4'
            except:
                try:
                    import PyQt5
                    patch_qt_on_import = 'PyQt5'
                except:
                    return

        if patch_qt_on_import:
            _patch_import_to_patch_pyqt_on_import(patch_qt_on_import)
        else:
            _internal_patch_qt()
        return


def _patch_import_to_patch_pyqt_on_import(patch_qt_on_import):
    dotted = patch_qt_on_import + '.'
    original_import = __import__
    from _pydev_imps._pydev_sys_patch import patch_sys_module, patch_reload, cancel_patches_in_sys_module
    patch_sys_module()
    patch_reload()

    def patched_import(name, *args, **kwargs):
        if patch_qt_on_import == name or name.startswith(dotted):
            builtins.__import__ = original_import
            cancel_patches_in_sys_module()
            _internal_patch_qt()
        return original_import(name, *args, **kwargs)

    try:
        import builtins
    except ImportError:
        import __builtin__ as builtins

    builtins.__import__ = patched_import


def _internal_patch_qt():
    try:
        from PySide import QtCore
    except:
        try:
            from PyQt4 import QtCore
        except:
            try:
                from PyQt5 import QtCore
            except:
                return

    _original_thread_init = QtCore.QThread.__init__
    _original_runnable_init = QtCore.QRunnable.__init__
    _original_QThread = QtCore.QThread

    class FuncWrapper:

        def __init__(self, original):
            self._original = original

        def __call__(self, *args, **kwargs):
            set_trace_in_qt()
            return self._original(*args, **kwargs)

    class StartedSignalWrapper:

        def __init__(self, thread, original_started):
            self.thread = thread
            self.original_started = original_started

        def connect(self, func, *args, **kwargs):
            return self.original_started.connect(FuncWrapper(func), *args, **kwargs)

        def disconnect(self, *args, **kwargs):
            return self.original_started.disconnect(*args, **kwargs)

        def emit(self, *args, **kwargs):
            return self.original_started.emit(*args, **kwargs)

    class ThreadWrapper(QtCore.QThread):

        def __init__(self, *args, **kwargs):
            _original_thread_init(self, *args, **kwargs)
            if self.__class__.run == _original_QThread.run:
                self.run = self._exec_run
            else:
                self._original_run = self.run
                self.run = self._new_run
            self._original_started = self.started
            self.started = StartedSignalWrapper(self, self.started)

        def _exec_run(self):
            set_trace_in_qt()
            self.exec_()
            return None

        def _new_run(self):
            set_trace_in_qt()
            return self._original_run()

    class RunnableWrapper(QtCore.QRunnable):

        def __init__(self, *args, **kwargs):
            _original_runnable_init(self, *args, **kwargs)
            self._original_run = self.run
            self.run = self._new_run

        def _new_run(self):
            set_trace_in_qt()
            return self._original_run()

    QtCore.QThread = ThreadWrapper
    QtCore.QRunnable = RunnableWrapper