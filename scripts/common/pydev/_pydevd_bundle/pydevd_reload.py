# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_reload.py
"""
Based on the python xreload.

Changes
======================

1. we don't recreate the old namespace from new classes. Rather, we keep the existing namespace,
load a new version of it and update only some of the things we can inplace. That way, we don't break
things such as singletons or end up with a second representation of the same class in memory.

2. If we find it to be a __metaclass__, we try to update it as a regular class.

3. We don't remove old attributes (and leave them lying around even if they're no longer used).

4. Reload hooks were changed

These changes make it more stable, especially in the common case (where in a debug session only the
contents of a function are changed), besides providing flexibility for users that want to extend
on it.



Hooks
======================

Classes/modules can be specially crafted to work with the reload (so that it can, for instance,
update some constant which was changed).

1. To participate in the change of some attribute:

    In a module:

    __xreload_old_new__(namespace, name, old, new)

    in a class:

    @classmethod
    __xreload_old_new__(cls, name, old, new)

    A class or module may include a method called '__xreload_old_new__' which is called when we're
    unable to reload a given attribute.



2. To do something after the whole reload is finished:

    In a module:

    __xreload_after_reload_update__(namespace):

    In a class:

    @classmethod
    __xreload_after_reload_update__(cls):


    A class or module may include a method called '__xreload_after_reload_update__' which is called
    after the reload finishes.


Important: when providing a hook, always use the namespace or cls provided and not anything in the global
namespace, as the global namespace are only temporarily created during the reload and may not reflect the
actual application state (while the cls and namespace passed are).


Current limitations
======================


- Attributes/constants are added, but not changed (so singletons and the application state is not
  broken -- use provided hooks to workaround it).

- Code using metaclasses may not always work.

- Functions and methods using decorators (other than classmethod and staticmethod) are not handled
  correctly.

- Renamings are not handled correctly.

- Dependent modules are not reloaded.

- New __slots__ can't be added to existing classes.


Info
======================

Original: http://svn.python.org/projects/sandbox/trunk/xreload/xreload.py
Note: it seems https://github.com/plone/plone.reload/blob/master/plone/reload/xreload.py enhances it (to check later)

Interesting alternative: https://code.google.com/p/reimport/

Alternative to reload().

This works by executing the module in a scratch namespace, and then patching classes, methods and
functions in place.  This avoids the need to patch instances.  New objects are copied into the
target namespace.

"""
import imp
from _pydev_bundle.pydev_imports import Exec
from _pydevd_bundle import pydevd_dont_trace
import sys
import traceback
import types
NO_DEBUG = 0
LEVEL1 = 1
LEVEL2 = 2
DEBUG = NO_DEBUG

def write(*args):
    new_lst = []
    for a in args:
        new_lst.append(str(a))

    msg = ' '.join(new_lst)
    sys.stdout.write('%s\n' % (msg,))


def write_err(*args):
    new_lst = []
    for a in args:
        new_lst.append(str(a))

    msg = ' '.join(new_lst)
    sys.stderr.write('pydev debugger: %s\n' % (msg,))


def notify_info0(*args):
    write_err(*args)


def notify_info(*args):
    if DEBUG >= LEVEL1:
        write(*args)


def notify_info2(*args):
    if DEBUG >= LEVEL2:
        write(*args)


def notify_error(*args):
    write_err(*args)


def code_objects_equal(code0, code1):
    for d in dir(code0):
        if d.startswith('_') or 'lineno' in d:
            continue
        if getattr(code0, d) != getattr(code1, d):
            return False

    return True


def xreload(mod):
    """Reload a module in place, updating classes, methods and functions.
    
    mod: a module object
    
    Returns a boolean indicating whether a change was done.
    """
    r = Reload(mod)
    r.apply()
    found_change = r.found_change
    r = None
    pydevd_dont_trace.clear_trace_filter_cache()
    return found_change


class Reload:

    def __init__(self, mod):
        self.mod = mod
        self.found_change = False

    def apply(self):
        mod = self.mod
        self._on_finish_callbacks = []
        try:
            modname = mod.__name__
            modns = mod.__dict__
            i = modname.rfind('.')
            if i >= 0:
                pkgname, modname = modname[:i], modname[i + 1:]
            else:
                pkgname = None
            if pkgname:
                pkg = sys.modules[pkgname]
                path = pkg.__path__
            else:
                pkg = None
                path = None
            stream, filename, (suffix, mode, kind) = imp.find_module(modname, path)
            try:
                if kind not in (imp.PY_COMPILED, imp.PY_SOURCE):
                    notify_error('Could not find source to reload (mod: %s)' % (modname,))
                    return
                if kind == imp.PY_SOURCE:
                    source = stream.read()
                    code = compile(source, filename, 'exec')
                else:
                    import marshal
                    code = marshal.load(stream)
            finally:
                if stream:
                    stream.close()

            new_namespace = modns.copy()
            new_namespace.clear()
            new_namespace['__name__'] = modns['__name__']
            Exec(code, new_namespace)
            oldnames = set(modns)
            newnames = set(new_namespace)
            for name in newnames - oldnames:
                notify_info0('Added:', name, 'to namespace')
                self.found_change = True
                modns[name] = new_namespace[name]

            for name in oldnames & newnames:
                self._update(modns, name, modns[name], new_namespace[name])

            self._handle_namespace(modns)
            for c in self._on_finish_callbacks:
                c()

            del self._on_finish_callbacks[:]
        except:
            traceback.print_exc()

        return

    def _handle_namespace(self, namespace, is_class_namespace = False):
        on_finish = None
        if is_class_namespace:
            xreload_after_update = getattr(namespace, '__xreload_after_reload_update__', None)
            if xreload_after_update is not None:
                self.found_change = True
                on_finish = lambda : xreload_after_update()
        elif '__xreload_after_reload_update__' in namespace:
            xreload_after_update = namespace['__xreload_after_reload_update__']
            self.found_change = True
            on_finish = lambda : xreload_after_update(namespace)
        if on_finish is not None:
            self._on_finish_callbacks.append(on_finish)
        return

    def _update(self, namespace, name, oldobj, newobj, is_class_namespace = False):
        """Update oldobj, if possible in place, with newobj.
        
        If oldobj is immutable, this simply returns newobj.
        
        Args:
          oldobj: the object to be updated
          newobj: the object used as the source for the update
        """
        try:
            notify_info2('Updating: ', oldobj)
            if oldobj is newobj:
                return
            if type(oldobj) is not type(newobj):
                notify_error('Type of: %s changed... Skipping.' % (oldobj,))
                return
            if isinstance(newobj, types.FunctionType):
                self._update_function(oldobj, newobj)
                return
            if isinstance(newobj, types.MethodType):
                self._update_method(oldobj, newobj)
                return
            if isinstance(newobj, classmethod):
                self._update_classmethod(oldobj, newobj)
                return
            if isinstance(newobj, staticmethod):
                self._update_staticmethod(oldobj, newobj)
                return
            if hasattr(types, 'ClassType'):
                classtype = (types.ClassType, type)
            else:
                classtype = type
            if isinstance(newobj, classtype):
                self._update_class(oldobj, newobj)
                return
            if hasattr(newobj, '__metaclass__') and hasattr(newobj, '__class__') and newobj.__metaclass__ == newobj.__class__:
                self._update_class(oldobj, newobj)
                return
            if namespace is not None:
                if oldobj != newobj and str(oldobj) != str(newobj) and repr(oldobj) != repr(newobj):
                    xreload_old_new = None
                    if is_class_namespace:
                        xreload_old_new = getattr(namespace, '__xreload_old_new__', None)
                        if xreload_old_new is not None:
                            self.found_change = True
                            xreload_old_new(name, oldobj, newobj)
                    elif '__xreload_old_new__' in namespace:
                        xreload_old_new = namespace['__xreload_old_new__']
                        xreload_old_new(namespace, name, oldobj, newobj)
                        self.found_change = True
        except:
            notify_error('Exception found when updating %s. Proceeding for other items.' % (name,))
            traceback.print_exc()

        return

    def _update_function(self, oldfunc, newfunc):
        """Update a function object."""
        oldfunc.__doc__ = newfunc.__doc__
        oldfunc.__dict__.update(newfunc.__dict__)
        try:
            newfunc.__code__
            attr_name = '__code__'
        except AttributeError:
            newfunc.func_code
            attr_name = 'func_code'

        old_code = getattr(oldfunc, attr_name)
        new_code = getattr(newfunc, attr_name)
        if not code_objects_equal(old_code, new_code):
            notify_info0('Updated function code:', oldfunc)
            setattr(oldfunc, attr_name, new_code)
            self.found_change = True
        try:
            oldfunc.__defaults__ = newfunc.__defaults__
        except AttributeError:
            oldfunc.func_defaults = newfunc.func_defaults

        return oldfunc

    def _update_method(self, oldmeth, newmeth):
        """Update a method object."""
        if hasattr(oldmeth, 'im_func') and hasattr(newmeth, 'im_func'):
            self._update(None, None, oldmeth.im_func, newmeth.im_func)
        elif hasattr(oldmeth, '__func__') and hasattr(newmeth, '__func__'):
            self._update(None, None, oldmeth.__func__, newmeth.__func__)
        return oldmeth

    def _update_class(self, oldclass, newclass):
        """Update a class object."""
        olddict = oldclass.__dict__
        newdict = newclass.__dict__
        oldnames = set(olddict)
        newnames = set(newdict)
        for name in newnames - oldnames:
            setattr(oldclass, name, newdict[name])
            notify_info0('Added:', name, 'to', oldclass)
            self.found_change = True

        for name in (oldnames & newnames) - set(['__dict__', '__doc__']):
            self._update(oldclass, name, olddict[name], newdict[name], is_class_namespace=True)

        old_bases = getattr(oldclass, '__bases__', None)
        new_bases = getattr(newclass, '__bases__', None)
        if str(old_bases) != str(new_bases):
            notify_error('Changing the hierarchy of a class is not supported. %s may be inconsistent.' % (oldclass,))
        self._handle_namespace(oldclass, is_class_namespace=True)
        return

    def _update_classmethod(self, oldcm, newcm):
        """Update a classmethod update."""
        self._update(None, None, oldcm.__get__(0), newcm.__get__(0))
        return

    def _update_staticmethod(self, oldsm, newsm):
        """Update a staticmethod update."""
        self._update(None, None, oldsm.__get__(0), newsm.__get__(0))
        return