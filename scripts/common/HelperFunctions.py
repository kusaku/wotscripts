# Embedded file name: scripts/common/HelperFunctions.py
import socket
from zlib import crc32
from itertools import ifilter
from uuid_utils import genUUID
import uuid
import time
import operator
import struct

def multiKeySorting(items, columns):
    from operator import itemgetter
    comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns ]

    def comparer(left, right):
        for fn, mult in comparers:
            if isinstance(fn(left), basestring):
                result = cmp(fn(left).lower(), fn(right).lower())
            else:
                result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0

    return sorted(items, cmp=comparer)


def wowpRound(value, precision):
    if precision <= 0:
        return int(value)
    precision = pow(10, precision)
    return int(precision * value) / float(precision)


def GetInMS(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%02d:%02d' % (m, s)


def findIf(container, predicate, default = None):
    """
    Finds the element in iterable container(i.e. list) the element using predicate
    @param container:
    @param predicate: function predicate
    @param default:
    @return: item or default
    """
    return next((item for item in container if predicate(item)), default)


def findSuitableIndex(container, predicate):
    """
    Finds the suitable index in iterable container(i.e. list) the element using predicate
    @param container: list container
    @param predicate: function predicate
    @return: suitable index or None
    """
    for i, item in enumerate(container):
        if predicate(item):
            return i

    return None


def select(*iterables):
    """
    Iterates through several iterable objects and return items
    @param iterables:
    """
    for iterable in iterables:
        for item in iterable:
            yield item


def generateID():
    newid = -1
    while newid <= 0:
        newid = crc32(str(genUUID()))

    return newid


def dictToKeyValueList(sourceDict):
    """
    @type sourceDict: dict
    @return: list of type [ {'key': <key>, 'value' : <value>}, ... ]
    """
    return [ {'key': k,
     'value': v} for k, v in sourceDict.iteritems() ]


def keyValueListToDict(sourceList):
    """
    @type sourceList: list of dict of type {'key'=<key>, 'value'=<value>}
    @return: dict
    """
    return dict(((d['key'], d['value']) for d in sourceList))


def minWithDefault(*args, **kwargs):
    """
    Built-in min function raises error if sequence is empty. This function
    will return default value if default is given.
    
    >>> minWithDefault([3,2,2,1,4,5])
    1
    >>> minWithDefault([])
    Traceback (most recent call last):
        ...
    ValueError: min() arg is an empty sequence
    >>> minWithDefault([], default=None)
    >>> minWithDefault([], default=0)
    0
    """
    key = kwargs.get('key')
    try:
        if key:
            return min(key=key, *args)
        return min(*args)
    except ValueError as e:
        if 'default' in kwargs:
            return kwargs.get('default')
        raise


def filter2(pred, seq):
    """
    
    >>> filter2(lambda e: e%2 == 0, [1,2,3,4,5,6,7])
    ([2, 4, 6], [1, 3, 5, 7])
    """
    A, B = [], []
    for e in seq:
        (A if pred(e) else B).append(e)

    return (A, B)


def calculateGlobalRating(bc, winsCount, survivesCount, totalXP, totalDamage, totalGroundDamage):
    """
    Calculates global(personal) player rating
    @param bc: total games played
    @param winsCount: total game wins
    @param survivesCount: total game survives
    @param totalXP: total gained base experience
    @param totalDamage: average damage dealt to enemy planes
    @param totalGroundDamage: average damage dealt to enemy ground objects
    @rtype: float
    >>> calculateGlobalRating(2443, 1251, 648, 28505, 600000, 0)
    2841.50765404571
    """
    if bc <= 0:
        return 0
    bc = float(bc)
    wins = min(winsCount / bc, 1.0)
    survives = min(survivesCount / bc, 1.0)
    xp = totalXP / bc
    dmg = totalDamage / bc
    grddmg = totalGroundDamage / bc
    import math
    return 540.0 * math.pow(bc, 0.37) * math.tanh(0.00163 * (3500.0 / (1 + math.exp(16.0 - 31.0 * wins)) + 1400.0 / (1 + math.exp(8.0 - 27.0 * survives)) + 3700.0 * math.asinh(0.0006 * (2.23 * (dmg + 0.032 * grddmg))) + math.tanh(0.002 * bc) * 3900.0 * math.asinh(0.0015 * xp)) / math.pow(bc, 0.37))


def createIMessage(msgtype, msgdata, msgtime = None, chain = 0, obid = -1, sendername = '', msgHeader = None):
    msgtime = msgtime if msgtime is not None else time.time()
    ob = dict(utcTime=msgtime, msgType=msgtype, msgData=msgdata, chain=chain, senderName=sendername)
    if msgHeader is not None:
        ob['msgHeader'] = msgHeader
    return (obid if obid != -1 else generateID(), ob)


def maxWithDefault(sequence, default = None, key = None):
    try:
        if key is None:
            return max(sequence)
        return max(sequence, key=key)
    except ValueError:
        return default

    return


def accumulate(iterable, func = operator.add):
    """Return running totals"""
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        total = func(total, element)
        yield total


def enumToString(enumCls, value):
    d = enumCls.__dict__
    for k, v in d.iteritems():
        if type(v) == int and v == value:
            return k

    return ''


def IPStrToUINT32(ip):
    return socket.htonl(struct.unpack('!I', socket.inet_aton(ip))[0])


def UINT32ToIPStr(st):
    st = '%08x' % st
    return '%i.%i.%i.%i' % (int(st[6:8], 16),
     int(st[4:6], 16),
     int(st[2:4], 16),
     int(st[0:2], 16))


if __name__ == '__main__':
    import doctest
    doctest.testmod()