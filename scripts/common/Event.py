# Embedded file name: scripts/common/Event.py
from debug_utils import *

class Event(object):

    def __init__(self, manager = None):
        self.__delegates = set()
        if manager is not None:
            manager.register(self)
        return

    def __call__(self, *args, **kw):
        for delegate in set(self.__delegates):
            try:
                delegate(*args, **kw)
            except:
                LOG_CURRENT_EXCEPTION()

    def __iadd__(self, delegate):
        self.__delegates.add(delegate)
        return self

    def __isub__(self, delegate):
        self.__delegates.discard(delegate)
        return self

    def clear(self):
        self.__delegates.clear()

    def __repr__(self):
        return 'Event(%s):%s' % (len(self.__delegates), repr(self.__delegates))

    def delegatesCount(self):
        return len(self.__delegates)


class EventOrdered(object):

    def __init__(self, manager = None):
        self.__delegates = list()
        if manager is not None:
            manager.register(self)
        return

    def __call__(self, *args, **kw):
        for delegate in self.__delegates:
            try:
                delegate(*args, **kw)
            except:
                LOG_CURRENT_EXCEPTION()

    def __iadd__(self, delegate):
        if delegate not in self.__delegates:
            self.__delegates.append(delegate)
        return self

    def __isub__(self, delegate):
        if delegate in self.__delegates:
            self.__delegates.remove(delegate)
        return self

    def clear(self):
        self.__delegates = list()

    def __repr__(self):
        return 'Event(%s):%s' % (len(self.__delegates), repr(self.__delegates))


class BlockingEvent(object):

    def __init__(self, manager = None):
        self.__delegates = list()
        if manager is not None:
            manager.register(self)
        return

    def insert(self, index, delegate):
        if delegate not in self.__delegates:
            self.__delegates.insert(index, delegate)

    def remove(self, delegate):
        self.__delegates.remove(delegate)

    def __call__(self, *args):
        for delegate in self.__delegates:
            try:
                if delegate(*args):
                    return True
            except:
                LOG_CURRENT_EXCEPTION()

        return False

    def __iadd__(self, delegate):
        if delegate not in self.__delegates:
            self.__delegates.append(delegate)
        return self

    def __isub__(self, delegate):
        self.__delegates.remove(delegate)
        return self

    def clear(self):
        self.__delegates[:] = []

    def __repr__(self):
        return 'Event(%s):%s' % (len(self.__delegates), repr(self.__delegates))


class Handler(object):

    def __init__(self, manager = None):
        self.__delegate = None
        if manager is not None:
            manager.register(self)
        return

    def __call__(self, *args):
        if self.__delegate is not None:
            return self.__delegate(*args)
        else:
            return

    def set(self, delegate):
        self.__delegate = delegate

    def clear(self):
        self.__delegate = None
        return


class EventManager(object):

    def __init__(self):
        self.__events = []

    def register(self, event):
        self.__events.append(event)

    def clear(self):
        for event in self.__events:
            event.clear()


class SmartProperty(object):

    def __init__(self, value):
        self.onChange = Event()
        self.value = value

    @property
    def value(self):
        if callable(self.__value):
            return self.__value()
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = val
        if val.__class__ is SmartProperty:
            val.onChange += self.onChange
        self.onChange()

    def __nonzero__(self):
        return bool(self.value)

    def __and__(self, other):
        res = SmartProperty(lambda : self.value and other.value)
        self.onChange += res.onChange
        other.onChange += res.onChange
        return res

    def __or__(self, other):
        res = SmartProperty(lambda : self.value or other.value)
        self.onChange += res.onChange
        other.onChange += res.onChange
        return res

    def __invert__(self):
        res = SmartProperty(lambda : not self.value)
        self.onChange += res.onChange
        return res