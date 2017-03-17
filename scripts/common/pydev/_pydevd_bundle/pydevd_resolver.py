# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_resolver.py
try:
    import StringIO
except:
    import io as StringIO

import traceback
from os.path import basename
try:
    __setFalse = False
except:
    import __builtin__
    setattr(__builtin__, 'True', 1)
    setattr(__builtin__, 'False', 0)

from _pydevd_bundle import pydevd_constants
from _pydevd_bundle.pydevd_constants import dict_iter_items, dict_keys, xrange
MAX_ITEMS_TO_HANDLE = 300
TOO_LARGE_MSG = 'Too large to show contents. Max items to show: ' + str(MAX_ITEMS_TO_HANDLE)
TOO_LARGE_ATTR = 'Unable to handle:'

class UnableToResolveVariableException(Exception):
    pass


class InspectStub:

    def isbuiltin(self, _args):
        return False

    def isroutine(self, object):
        return False


try:
    import inspect
except:
    inspect = InspectStub()

try:
    import java.lang
except:
    pass

try:
    MethodWrapperType = type([].__str__)
except:
    MethodWrapperType = None

class AbstractResolver:
    """
        This class exists only for documentation purposes to explain how to create a resolver.
    
        Some examples on how to resolve things:
        - list: get_dictionary could return a dict with index->item and use the index to resolve it later
        - set: get_dictionary could return a dict with id(object)->object and reiterate in that array to resolve it later
        - arbitrary instance: get_dictionary could return dict with attr_name->attr and use getattr to resolve it later
    """

    def resolve(self, var, attribute):
        """
            In this method, we'll resolve some child item given the string representation of the item in the key
            representing the previously asked dictionary.
        
            @param var: this is the actual variable to be resolved.
            @param attribute: this is the string representation of a key previously returned in get_dictionary.
        """
        raise NotImplementedError

    def get_dictionary(self, var):
        """
            @param var: this is the variable that should have its children gotten.
        
            @return: a dictionary where each pair key, value should be shown to the user as children items
            in the variables view for the given var.
        """
        raise NotImplementedError


class DefaultResolver:
    """
        DefaultResolver is the class that'll actually resolve how to show some variable.
    """

    def resolve(self, var, attribute):
        return getattr(var, attribute)

    def get_dictionary(self, var):
        if MethodWrapperType:
            return self._getPyDictionary(var)
        else:
            return self._getJyDictionary(var)

    def _getJyDictionary(self, obj):
        ret = {}
        found = java.util.HashMap()
        original = obj
        if hasattr(obj, '__class__') and obj.__class__ == java.lang.Class:
            classes = []
            classes.append(obj)
            c = obj.getSuperclass()
            while c != None:
                classes.append(c)
                c = c.getSuperclass()

            interfs = []
            for obj in classes:
                interfs.extend(obj.getInterfaces())

            classes.extend(interfs)
            for obj in classes:
                declaredMethods = obj.getDeclaredMethods()
                declaredFields = obj.getDeclaredFields()
                for i in xrange(len(declaredMethods)):
                    name = declaredMethods[i].getName()
                    ret[name] = declaredMethods[i].toString()
                    found.put(name, 1)

                for i in xrange(len(declaredFields)):
                    name = declaredFields[i].getName()
                    found.put(name, 1)
                    declaredFields[i].setAccessible(True)
                    try:
                        ret[name] = declaredFields[i].get(original)
                    except:
                        ret[name] = declaredFields[i].toString()

        try:
            d = dir(original)
            for name in d:
                if found.get(name) is not 1:
                    ret[name] = getattr(original, name)

        except:
            pass

        return ret

    def _getPyDictionary(self, var):
        filterPrivate = False
        filterSpecial = True
        filterFunction = True
        filterBuiltIn = True
        names = dir(var)
        if not names and hasattr(var, '__members__'):
            names = var.__members__
        d = {}
        if filterBuiltIn or filterFunction:
            for n in names:
                if filterSpecial:
                    if n.startswith('__') and n.endswith('__'):
                        continue
                if filterPrivate:
                    if n.startswith('_') or n.endswith('__'):
                        continue
                try:
                    attr = getattr(var, n)
                    if filterBuiltIn:
                        if inspect.isbuiltin(attr):
                            continue
                    if filterFunction:
                        if inspect.isroutine(attr) or isinstance(attr, MethodWrapperType):
                            continue
                except:
                    strIO = StringIO.StringIO()
                    traceback.print_exc(file=strIO)
                    attr = strIO.getvalue()

                d[n] = attr

        return d


class DictResolver:

    def resolve(self, dict, key):
        if key in ('__len__', TOO_LARGE_ATTR):
            return None
        else:
            if '(' not in key:
                try:
                    return dict[key]
                except:
                    return getattr(dict, key)

            expected_id = int(key.split('(')[-1][:-1])
            for key, val in dict_iter_items(dict):
                if id(key) == expected_id:
                    return val

            raise UnableToResolveVariableException()
            return None

    def key_to_str(self, key):
        if isinstance(key, str):
            return '%r' % key
        else:
            if not pydevd_constants.IS_PY3K:
                if isinstance(key, unicode):
                    return "u'%s'" % key
            return key

    def get_dictionary(self, dict):
        ret = {}
        i = 0
        for key, val in dict_iter_items(dict):
            i += 1
            key = '%s (%s)' % (self.key_to_str(key), id(key))
            ret[key] = val
            if i > MAX_ITEMS_TO_HANDLE:
                ret[TOO_LARGE_ATTR] = TOO_LARGE_MSG
                break

        ret['__len__'] = len(dict)
        additional_fields = defaultResolver.get_dictionary(dict)
        ret.update(additional_fields)
        return ret


class TupleResolver:

    def resolve(self, var, attribute):
        """
            @param var: that's the original attribute
            @param attribute: that's the key passed in the dict (as a string)
        """
        if attribute in ('__len__', TOO_LARGE_ATTR):
            return None
        else:
            try:
                return var[int(attribute)]
            except:
                return getattr(var, attribute)

            return None

    def get_dictionary(self, var):
        l = len(var)
        d = {}
        format_str = '%0' + str(int(len(str(l)))) + 'd'
        i = 0
        for item in var:
            d[format_str % i] = item
            i += 1
            if i > MAX_ITEMS_TO_HANDLE:
                d[TOO_LARGE_ATTR] = TOO_LARGE_MSG
                break

        d['__len__'] = len(var)
        additional_fields = defaultResolver.get_dictionary(var)
        d.update(additional_fields)
        return d


class SetResolver:
    """
        Resolves a set as dict id(object)->object
    """

    def resolve(self, var, attribute):
        if attribute in ('__len__', TOO_LARGE_ATTR):
            return None
        else:
            try:
                attribute = int(attribute)
            except:
                return getattr(var, attribute)

            for v in var:
                if id(v) == attribute:
                    return v

            raise UnableToResolveVariableException('Unable to resolve %s in %s' % (attribute, var))
            return None

    def get_dictionary(self, var):
        d = {}
        i = 0
        for item in var:
            i += 1
            d[id(item)] = item
            if i > MAX_ITEMS_TO_HANDLE:
                d[TOO_LARGE_ATTR] = TOO_LARGE_MSG
                break

        d['__len__'] = len(var)
        additional_fields = defaultResolver.get_dictionary(var)
        d.update(additional_fields)
        return d


class InstanceResolver:

    def resolve(self, var, attribute):
        field = var.__class__.getDeclaredField(attribute)
        field.setAccessible(True)
        return field.get(var)

    def get_dictionary(self, obj):
        ret = {}
        declaredFields = obj.__class__.getDeclaredFields()
        for i in xrange(len(declaredFields)):
            name = declaredFields[i].getName()
            try:
                declaredFields[i].setAccessible(True)
                ret[name] = declaredFields[i].get(obj)
            except:
                traceback.print_exc()

        return ret


class JyArrayResolver:
    """
        This resolves a regular Object[] array from java
    """

    def resolve(self, var, attribute):
        if attribute == '__len__':
            return None
        else:
            return var[int(attribute)]

    def get_dictionary(self, obj):
        ret = {}
        for i in xrange(len(obj)):
            ret[i] = obj[i]

        ret['__len__'] = len(obj)
        return ret


class NdArrayResolver:
    """
        This resolves a numpy ndarray returning some metadata about the NDArray
    """

    def is_numeric(self, obj):
        if not hasattr(obj, 'dtype'):
            return False
        return obj.dtype.kind in 'biufc'

    def resolve(self, obj, attribute):
        if attribute == '__internals__':
            return defaultResolver.get_dictionary(obj)
        if attribute == 'min':
            if self.is_numeric(obj):
                return obj.min()
            else:
                return None
        if attribute == 'max':
            if self.is_numeric(obj):
                return obj.max()
            else:
                return None
        if attribute == 'shape':
            return obj.shape
        elif attribute == 'dtype':
            return obj.dtype
        elif attribute == 'size':
            return obj.size
        elif attribute.startswith('['):
            container = NdArrayItemsContainer()
            i = 0
            format_str = '%0' + str(int(len(str(len(obj))))) + 'd'
            for item in obj:
                setattr(container, format_str % i, item)
                i += 1
                if i > MAX_ITEMS_TO_HANDLE:
                    setattr(container, TOO_LARGE_ATTR, TOO_LARGE_MSG)
                    break

            return container
        else:
            return None

    def get_dictionary(self, obj):
        ret = dict()
        ret['__internals__'] = defaultResolver.get_dictionary(obj)
        if obj.size > 1048576:
            ret['min'] = 'ndarray too big, calculating min would slow down debugging'
            ret['max'] = 'ndarray too big, calculating max would slow down debugging'
        elif self.is_numeric(obj):
            ret['min'] = obj.min()
            ret['max'] = obj.max()
        else:
            ret['min'] = 'not a numeric object'
            ret['max'] = 'not a numeric object'
        ret['shape'] = obj.shape
        ret['dtype'] = obj.dtype
        ret['size'] = obj.size
        ret['[0:%s] ' % len(obj)] = list(obj[0:MAX_ITEMS_TO_HANDLE])
        return ret


class NdArrayItemsContainer:
    pass


class MultiValueDictResolver(DictResolver):

    def resolve(self, dict, key):
        if key in ('__len__', TOO_LARGE_ATTR):
            return None
        else:
            expected_id = int(key.split('(')[-1][:-1])
            for key in dict_keys(dict):
                val = dict.getlist(key)
                if id(key) == expected_id:
                    return val

            raise UnableToResolveVariableException()
            return None

    def get_dictionary(self, dict):
        ret = {}
        i = 0
        for key in dict_keys(dict):
            val = dict.getlist(key)
            i += 1
            key = '%s (%s)' % (self.key_to_str(key), id(key))
            ret[key] = val
            if i > MAX_ITEMS_TO_HANDLE:
                ret[TOO_LARGE_ATTR] = TOO_LARGE_MSG
                break

        ret['__len__'] = len(dict)
        return ret


class DequeResolver(TupleResolver):

    def get_dictionary(self, var):
        d = TupleResolver.get_dictionary(self, var)
        d['maxlen'] = getattr(var, 'maxlen', None)
        return d


class FrameResolver:
    """
    This resolves a frame.
    """

    def resolve(self, obj, attribute):
        if attribute == '__internals__':
            return defaultResolver.get_dictionary(obj)
        elif attribute == 'stack':
            return self.get_frame_stack(obj)
        elif attribute == 'f_locals':
            return obj.f_locals
        else:
            return None

    def get_dictionary(self, obj):
        ret = dict()
        ret['__internals__'] = defaultResolver.get_dictionary(obj)
        ret['stack'] = self.get_frame_stack(obj)
        ret['f_locals'] = obj.f_locals
        return ret

    def get_frame_stack(self, frame):
        ret = []
        if frame is not None:
            ret.append(self.get_frame_name(frame))
            while frame.f_back:
                frame = frame.f_back
                ret.append(self.get_frame_name(frame))

        return ret

    def get_frame_name(self, frame):
        if frame is None:
            return 'None'
        else:
            try:
                name = basename(frame.f_code.co_filename)
                return 'frame: %s [%s:%s]  id:%s' % (frame.f_code.co_name,
                 name,
                 frame.f_lineno,
                 id(frame))
            except:
                return 'frame object'

            return


defaultResolver = DefaultResolver()
dictResolver = DictResolver()
tupleResolver = TupleResolver()
instanceResolver = InstanceResolver()
jyArrayResolver = JyArrayResolver()
setResolver = SetResolver()
ndarrayResolver = NdArrayResolver()
multiValueDictResolver = MultiValueDictResolver()
dequeResolver = DequeResolver()
frameResolver = FrameResolver()