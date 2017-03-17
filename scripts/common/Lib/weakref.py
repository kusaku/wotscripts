# Embedded file name: scripts/common/Lib/weakref.py
"""Weak reference support for Python.

This module is an implementation of PEP 205:

http://www.python.org/dev/peps/pep-0205/
"""
import UserDict
from _weakref import getweakrefcount, getweakrefs, ref, proxy, CallableProxyType, ProxyType, ReferenceType
from _weakrefset import WeakSet
from exceptions import ReferenceError
ProxyTypes = (ProxyType, CallableProxyType)
__all__ = ['ref',
 'proxy',
 'getweakrefcount',
 'getweakrefs',
 'WeakKeyDictionary',
 'ReferenceError',
 'ReferenceType',
 'ProxyType',
 'CallableProxyType',
 'ProxyTypes',
 'WeakValueDictionary',
 'WeakSet']

class WeakValueDictionary(UserDict.UserDict):
    """Mapping class that references values weakly.
    
    Entries in the dictionary will be discarded when no strong
    reference to the value exists anymore
    """

    def __init__(self, *args, **kw):

        def remove(wr, selfref = ref(self)):
            self = selfref()
            if self is not None:
                del self.data[wr.key]
            return

        self._remove = remove
        UserDict.UserDict.__init__(self, *args, **kw)

    def __getitem__(self, key):
        o = self.data[key]()
        if o is None:
            raise KeyError, key
        else:
            return o
        return

    def __contains__(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False

        return o is not None

    def has_key(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False

        return o is not None

    def __repr__(self):
        return '<WeakValueDictionary at %s>' % id(self)

    def __setitem__(self, key, value):
        self.data[key] = KeyedRef(value, self._remove, key)

    def copy(self):
        new = WeakValueDictionary()
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                new[key] = o

        return new

    __copy__ = copy

    def __deepcopy__(self, memo):
        from copy import deepcopy
        new = self.__class__()
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                new[deepcopy(key, memo)] = o

        return new

    def get(self, key, default = None):
        try:
            wr = self.data[key]
        except KeyError:
            return default

        o = wr()
        if o is None:
            return default
        else:
            return o
            return

    def items(self):
        L = []
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                L.append((key, o))

        return L

    def iteritems(self):
        for wr in self.data.itervalues():
            value = wr()
            if value is not None:
                yield (wr.key, value)

        return

    def iterkeys(self):
        return self.data.iterkeys()

    def __iter__(self):
        return self.data.iterkeys()

    def itervaluerefs(self):
        """Return an iterator that yields the weak references to the values.
        
        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.
        
        """
        return self.data.itervalues()

    def itervalues(self):
        for wr in self.data.itervalues():
            obj = wr()
            if obj is not None:
                yield obj

        return

    def popitem--- This code section failed: ---

0	SETUP_LOOP        '59'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'popitem'
12	CALL_FUNCTION_0   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'key'
21	STORE_FAST        'wr'

24	LOAD_FAST         'wr'
27	CALL_FUNCTION_0   None
30	STORE_FAST        'o'

33	LOAD_FAST         'o'
36	LOAD_CONST        None
39	COMPARE_OP        'is not'
42	POP_JUMP_IF_FALSE '3'

45	LOAD_FAST         'key'
48	LOAD_FAST         'o'
51	BUILD_TUPLE_2     None
54	RETURN_END_IF     None
55	JUMP_BACK         '3'
58	POP_BLOCK         None
59_0	COME_FROM         '0'
59	LOAD_CONST        None
62	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 58

    def pop(self, key, *args):
        try:
            o = self.data.pop(key)()
        except KeyError:
            if args:
                return args[0]
            raise

        if o is None:
            raise KeyError, key
        else:
            return o
        return

    def setdefault(self, key, default = None):
        try:
            wr = self.data[key]
        except KeyError:
            self.data[key] = KeyedRef(default, self._remove, key)
            return default

        return wr()

    def update(self, dict = None, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, 'items'):
                dict = type({})(dict)
            for key, o in dict.items():
                d[key] = KeyedRef(o, self._remove, key)

        if len(kwargs):
            self.update(kwargs)
        return

    def valuerefs(self):
        """Return a list of weak references to the values.
        
        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.
        
        """
        return self.data.values()

    def values(self):
        L = []
        for wr in self.data.values():
            o = wr()
            if o is not None:
                L.append(o)

        return L


class KeyedRef(ref):
    """Specialized reference that includes a key corresponding to the value.
    
    This is used in the WeakValueDictionary to avoid having to create
    a function object for each key stored in the mapping.  A shared
    callback object can use the 'key' attribute of a KeyedRef instead
    of getting a reference to the key from an enclosing scope.
    
    """
    __slots__ = ('key',)

    def __new__(type, ob, callback, key):
        self = ref.__new__(type, ob, callback)
        self.key = key
        return self

    def __init__(self, ob, callback, key):
        super(KeyedRef, self).__init__(ob, callback)


class WeakKeyDictionary(UserDict.UserDict):
    """ Mapping class that references keys weakly.
    
    Entries in the dictionary will be discarded when there is no
    longer a strong reference to the key. This can be used to
    associate additional data with an object owned by other parts of
    an application without adding attributes to those objects. This
    can be especially useful with objects that override attribute
    accesses.
    """

    def __init__(self, dict = None):
        self.data = {}

        def remove(k, selfref = ref(self)):
            self = selfref()
            if self is not None:
                del self.data[k]
            return

        self._remove = remove
        if dict is not None:
            self.update(dict)
        return

    def __delitem__(self, key):
        del self.data[ref(key)]

    def __getitem__(self, key):
        return self.data[ref(key)]

    def __repr__(self):
        return '<WeakKeyDictionary at %s>' % id(self)

    def __setitem__(self, key, value):
        self.data[ref(key, self._remove)] = value

    def copy(self):
        new = WeakKeyDictionary()
        for key, value in self.data.items():
            o = key()
            if o is not None:
                new[o] = value

        return new

    __copy__ = copy

    def __deepcopy__(self, memo):
        from copy import deepcopy
        new = self.__class__()
        for key, value in self.data.items():
            o = key()
            if o is not None:
                new[o] = deepcopy(value, memo)

        return new

    def get(self, key, default = None):
        return self.data.get(ref(key), default)

    def has_key(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0

        return wr in self.data

    def __contains__(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0

        return wr in self.data

    def items(self):
        L = []
        for key, value in self.data.items():
            o = key()
            if o is not None:
                L.append((o, value))

        return L

    def iteritems(self):
        for wr, value in self.data.iteritems():
            key = wr()
            if key is not None:
                yield (key, value)

        return

    def iterkeyrefs(self):
        """Return an iterator that yields the weak references to the keys.
        
        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the keys around longer than needed.
        
        """
        return self.data.iterkeys()

    def iterkeys(self):
        for wr in self.data.iterkeys():
            obj = wr()
            if obj is not None:
                yield obj

        return

    def __iter__(self):
        return self.iterkeys()

    def itervalues(self):
        return self.data.itervalues()

    def keyrefs(self):
        """Return a list of weak references to the keys.
        
        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the keys around longer than needed.
        
        """
        return self.data.keys()

    def keys(self):
        L = []
        for wr in self.data.keys():
            o = wr()
            if o is not None:
                L.append(o)

        return L

    def popitem--- This code section failed: ---

0	SETUP_LOOP        '59'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'data'
9	LOAD_ATTR         'popitem'
12	CALL_FUNCTION_0   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'key'
21	STORE_FAST        'value'

24	LOAD_FAST         'key'
27	CALL_FUNCTION_0   None
30	STORE_FAST        'o'

33	LOAD_FAST         'o'
36	LOAD_CONST        None
39	COMPARE_OP        'is not'
42	POP_JUMP_IF_FALSE '3'

45	LOAD_FAST         'o'
48	LOAD_FAST         'value'
51	BUILD_TUPLE_2     None
54	RETURN_END_IF     None
55	JUMP_BACK         '3'
58	POP_BLOCK         None
59_0	COME_FROM         '0'
59	LOAD_CONST        None
62	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 58

    def pop(self, key, *args):
        return self.data.pop(ref(key), *args)

    def setdefault(self, key, default = None):
        return self.data.setdefault(ref(key, self._remove), default)

    def update(self, dict = None, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, 'items'):
                dict = type({})(dict)
            for key, value in dict.items():
                d[ref(key, self._remove)] = value

        if len(kwargs):
            self.update(kwargs)
        return