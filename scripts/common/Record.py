# Embedded file name: scripts/common/Record.py


class Record(object):
    __slots__ = ()

    def __init__(self, **kwargs):
        for fieldName, value in kwargs.iteritems():
            setattr(self, fieldName, value)

    def items(self):
        return [ (fieldName, getattr(self, fieldName)) for fieldName in self.__slots__ ]

    def __iter__(self):
        for fieldName in self.__slots__:
            yield getattr(self, fieldName)

    def __getitem__(self, index):
        return getattr(self, self.__slots__[index])