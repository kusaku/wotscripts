# Embedded file name: scripts/common/pydev/_pydev_bundle/_pydev_tipper_common.py
try:
    import inspect
except:
    try:
        from _pydev_imps import _pydev_inspect as inspect
    except:
        import traceback
        traceback.print_exc()

try:
    import re
except:
    try:
        import sre as re
    except:
        import traceback
        traceback.print_exc()

from _pydevd_bundle.pydevd_constants import xrange

def do_find(f, mod):
    import linecache
    if inspect.ismodule(mod):
        return (f, 0, 0)
    else:
        lines = linecache.getlines(f)
        if inspect.isclass(mod):
            name = mod.__name__
            pat = re.compile('^\\s*class\\s*' + name + '\\b')
            for i in xrange(len(lines)):
                if pat.match(lines[i]):
                    return (f, i, 0)

            return (f, 0, 0)
        if inspect.ismethod(mod):
            mod = mod.im_func
        if inspect.isfunction(mod):
            try:
                mod = mod.func_code
            except AttributeError:
                mod = mod.__code__

        if inspect.istraceback(mod):
            mod = mod.tb_frame
        if inspect.isframe(mod):
            mod = mod.f_code
        if inspect.iscode(mod):
            if not hasattr(mod, 'co_filename'):
                return (None, 0, 0)
            if not hasattr(mod, 'co_firstlineno'):
                return (mod.co_filename, 0, 0)
            lnum = mod.co_firstlineno
            pat = re.compile('^(\\s*def\\s)|(.*(?<!\\w)lambda(:|\\s))|^(\\s*@)')
            while lnum > 0:
                if pat.match(lines[lnum]):
                    break
                lnum -= 1

            return (f, lnum, 0)
        raise RuntimeError('Do not know about: ' + f + ' ' + str(mod))
        return