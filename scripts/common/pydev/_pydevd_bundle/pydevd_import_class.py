# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_import_class.py
import sys

def _imp(name, log = None):
    try:
        return __import__(name)
    except:
        if '.' in name:
            sub = name[0:name.rfind('.')]
            if log is not None:
                log.add_content('Unable to import', name, 'trying with', sub)
                log.add_exception()
            return _imp(sub, log)
        s = 'Unable to import module: %s - sys.path: %s' % (str(name), sys.path)
        if log is not None:
            log.add_content(s)
            log.add_exception()
        raise ImportError(s)

    return


IS_IPY = False
if sys.platform == 'cli':
    IS_IPY = True
    _old_imp = _imp

    def _imp(name, log = None):
        import clr
        initial_name = name
        while '.' in name:
            try:
                clr.AddReference(name)
                break
            except:
                name = name[0:name.rfind('.')]

        else:
            try:
                clr.AddReference(name)
            except:
                pass

        return _old_imp(initial_name, log)


def import_name(name, log = None):
    mod = _imp(name, log)
    components = name.split('.')
    old_comp = None
    for comp in components[1:]:
        try:
            mod = getattr(mod, comp)
        except AttributeError:
            if old_comp != comp:
                raise

        old_comp = comp

    return mod