# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_cython_wrapper.py
try:
    from _pydevd_bundle.pydevd_cython import trace_dispatch, PyDBAdditionalThreadInfo
except ImportError:
    try:
        import struct
        import sys
        try:
            is_python_64bit = struct.calcsize('P') == 8
        except:
            raise ImportError

        plat = '32'
        if is_python_64bit:
            plat = '64'
        mod_name = 'pydevd_cython_%s_%s%s_%s' % (sys.platform,
         sys.version_info[0],
         sys.version_info[1],
         plat)
        check_name = '_pydevd_bundle.%s' % (mod_name,)
        mod = __import__(check_name)
        mod = getattr(mod, mod_name)
        trace_dispatch, PyDBAdditionalThreadInfo = mod.trace_dispatch, mod.PyDBAdditionalThreadInfo
    except ImportError:
        raise