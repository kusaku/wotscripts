# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_trace_dispatch.py
import os
use_cython = os.getenv('PYDEVD_USE_CYTHON', None)
import sys
if use_cython == 'YES':
    from _pydevd_bundle.pydevd_cython_wrapper import trace_dispatch as _trace_dispatch

    def trace_dispatch(py_db, frame, event, arg):
        return _trace_dispatch(py_db, frame, event, arg)


elif use_cython == 'NO':
    from _pydevd_bundle.pydevd_trace_dispatch_regular import trace_dispatch
elif use_cython is None:
    try:
        from _pydevd_bundle.pydevd_cython_wrapper import trace_dispatch as _trace_dispatch

        def trace_dispatch(py_db, frame, event, arg):
            return _trace_dispatch(py_db, frame, event, arg)


    except ImportError:
        from _pydevd_bundle.pydevd_additional_thread_info_regular import PyDBAdditionalThreadInfo
        from _pydevd_bundle.pydevd_trace_dispatch_regular import trace_dispatch
        from _pydevd_bundle.pydevd_constants import CYTHON_SUPPORTED
        if CYTHON_SUPPORTED:
            from _pydev_bundle.pydev_monkey import log_error_once
            log_error_once('warning: Debugger speedups using cython not found. Run \'"%s" "%s" build_ext --inplace\' to build.' % (sys.executable, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'setup_cython.py')))

else:
    raise RuntimeError('Unexpected value for PYDEVD_USE_CYTHON: %s (accepted: YES, NO)' % (use_cython,))