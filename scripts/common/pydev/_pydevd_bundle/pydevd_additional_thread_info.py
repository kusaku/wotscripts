# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_additional_thread_info.py
import os
use_cython = os.getenv('PYDEVD_USE_CYTHON', None)
if use_cython == 'YES':
    from _pydevd_bundle.pydevd_cython_wrapper import PyDBAdditionalThreadInfo
elif use_cython == 'NO':
    from _pydevd_bundle.pydevd_additional_thread_info_regular import PyDBAdditionalThreadInfo
elif use_cython is None:
    try:
        from _pydevd_bundle.pydevd_cython_wrapper import PyDBAdditionalThreadInfo
    except ImportError:
        from _pydevd_bundle.pydevd_additional_thread_info_regular import PyDBAdditionalThreadInfo

else:
    raise RuntimeError('Unexpected value for PYDEVD_USE_CYTHON: %s (accepted: YES, NO)' % (use_cython,))