# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_constants.py
"""
This module holds the constants used for specifying the states of the debugger.
"""
from __future__ import nested_scopes
STATE_RUN = 1
STATE_SUSPEND = 2
PYTHON_SUSPEND = 1
DJANGO_SUSPEND = 2
JINJA2_SUSPEND = 3
try:
    __setFalse = False
except:
    import __builtin__
    setattr(__builtin__, 'True', 1)
    setattr(__builtin__, 'False', 0)

class DebugInfoHolder:
    DEBUG_RECORD_SOCKET_READS = False
    DEBUG_TRACE_LEVEL = -1
    DEBUG_TRACE_BREAKPOINTS = -1


import sys
try:
    get_frame = sys._getframe
except AttributeError:

    def get_frame():
        raise AssertionError('sys._getframe not available (possible causes: enable -X:Frames on IronPython?)')


MAXIMUM_VARIABLE_REPRESENTATION_SIZE = 1000
import os
from _pydevd_bundle import pydevd_vm_type
IS_JYTHON = pydevd_vm_type.get_vm_type() == pydevd_vm_type.PydevdVmType.JYTHON
IS_JYTH_LESS25 = False
if IS_JYTHON:
    if sys.version_info[0] == 2 and sys.version_info[1] < 5:
        IS_JYTH_LESS25 = True
CYTHON_SUPPORTED = False
try:
    import platform
    python_implementation = platform.python_implementation()
except:
    pass
else:
    if python_implementation == 'CPython':
        if sys.version_info[0] == 2 and sys.version_info[1] >= 7 or sys.version_info[0] == 3 and sys.version_info[1] >= 3 or sys.version_info[0] > 3:
            CYTHON_SUPPORTED = True

IS_PY3K = False
IS_PY34_OLDER = False
IS_PY2 = True
IS_PY27 = False
IS_PY24 = False
try:
    if sys.version_info[0] >= 3:
        IS_PY3K = True
        IS_PY2 = False
        if sys.version_info[0] == 3 and sys.version_info[1] >= 4 or sys.version_info[0] > 3:
            IS_PY34_OLDER = True
    elif sys.version_info[0] == 2 and sys.version_info[1] == 7:
        IS_PY27 = True
    elif sys.version_info[0] == 2 and sys.version_info[1] == 4:
        IS_PY24 = True
except AttributeError:
    pass

try:
    SUPPORT_GEVENT = os.getenv('GEVENT_SUPPORT', 'False') == 'True'
except:
    SUPPORT_GEVENT = False

USE_LIB_COPY = SUPPORT_GEVENT and not IS_PY3K and sys.version_info[1] >= 6
from _pydev_imps import _pydev_threading as threading
from _pydev_imps import _pydev_thread
_nextThreadIdLock = _pydev_thread.allocate_lock()
try:
    dict_contains = dict.has_key
except:
    try:
        dict_contains = dict.__contains__
    except:
        try:
            dict_contains = dict.has_key
        except NameError:

            def dict_contains(d, key):
                return d.has_key(key)


try:
    dict_pop = dict.pop
except:

    def dict_pop(d, key, default = None):
        try:
            ret = d[key]
            del d[key]
            return ret
        except:
            return default


if IS_PY3K:

    def dict_keys(d):
        return list(d.keys())


    def dict_values(d):
        return list(d.values())


    dict_iter_values = dict.values

    def dict_iter_items(d):
        return d.items()


    def dict_items(d):
        return list(d.items())


else:
    try:
        dict_keys = dict.keys
    except:

        def dict_keys(d):
            return d.keys()


    try:
        dict_iter_values = dict.itervalues
    except:
        try:
            dict_iter_values = dict.values
        except:

            def dict_iter_values(d):
                return d.values()


    try:
        dict_values = dict.values
    except:

        def dict_values(d):
            return d.values()


    def dict_iter_items(d):
        try:
            return d.iteritems()
        except:
            return d.items()


    def dict_items(d):
        return d.items()


try:
    xrange = xrange
except:
    xrange = range

try:
    import itertools
    izip = itertools.izip
except:
    izip = zip

try:
    object
except NameError:

    class object:
        pass


    import __builtin__
    setattr(__builtin__, 'object', object)

try:
    enumerate
except:

    def enumerate(lst):
        ret = []
        i = 0
        for element in lst:
            ret.append((i, element))
            i += 1

        return ret


try:
    from StringIO import StringIO
except:
    from io import StringIO

def get_pid():
    try:
        return os.getpid()
    except AttributeError:
        try:
            import java.lang.management.ManagementFactory
            pid = java.lang.management.ManagementFactory.getRuntimeMXBean().getName()
            return pid.replace('@', '_')
        except:
            return '000001'


def clear_cached_thread_id(thread):
    try:
        del thread.__pydevd_id__
    except AttributeError:
        pass


def get_thread_id(thread):
    try:
        tid = thread.__pydevd_id__
        if tid is None:
            raise AttributeError()
    except AttributeError:
        _nextThreadIdLock.acquire()
        try:
            tid = getattr(thread, '__pydevd_id__', None)
            if tid is None:
                pid = get_pid()
                try:
                    tid = thread.__pydevd_id__ = 'pid_%s_id_%s' % (pid, thread.get_ident())
                except:
                    tid = thread.__pydevd_id__ = 'pid_%s_id_%s' % (pid, id(thread))

        finally:
            _nextThreadIdLock.release()

    return tid


class Null:
    """
    Gotten from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/68205
    """

    def __init__(self, *args, **kwargs):
        return None

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, mname):
        if len(mname) > 4 and mname[:2] == '__' and mname[-2:] == '__':
            raise AttributeError(mname)
        return self

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self

    def __repr__(self):
        return '<Null>'

    def __str__(self):
        return 'Null'

    def __len__(self):
        return 0

    def __getitem__(self):
        return self

    def __setitem__(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def __nonzero__(self):
        return 0

    def __iter__(self):
        return iter(())


def call_only_once(func):
    """
    To be used as a decorator
    
    @call_only_once
    def func():
        print 'Calling func only this time'
    
    Actually, in PyDev it must be called as:
    
    func = call_only_once(func) to support older versions of Python.
    """

    def new_func(*args, **kwargs):
        if not new_func._called:
            new_func._called = True
            return func(*args, **kwargs)

    new_func._called = False
    return new_func


if __name__ == '__main__':
    if Null():
        sys.stdout.write('here\n')