# Embedded file name: scripts/common/wgPickle.py
import cPickle
import JsonPickle
import zlib
import time
import re
import msgpack
import Math
from config_consts import IS_DEVELOPMENT
AUTO_COMPRESS_LENGTH = 100
JSON_LOADS_MAX_STRING_SIZE = 10240
MSGPACK_LOADS_MAX_STRING_SIZE = 51200
COMPRESS_LEVEL = 9
COMPRESS_PREFIX = 'z'
PLAIN_PREFIX = 'n'
MESSAGE_MATCHER = re.compile('(_)([%s%s])(.*)' % (COMPRESS_PREFIX, PLAIN_PREFIX), re.DOTALL)
MESSAGE_FORMAT = '_%s%s'
PICKLER_LOG = {}
LOG_ENABLED = IS_DEVELOPMENT
FromClientToServer = 0
FromClientToClient = 1
FromServerToServer = 2
FromServerToClient = 3
MsgPack = 4
MSGPACK_CLASSES_ENCODER = {Math.Vector3: {'__class__': JsonPickle.classNameFormatter,
                'args': JsonPickle.mathVectorArgs},
 Math.Vector4: {'__class__': JsonPickle.classNameFormatter,
                'args': JsonPickle.mathVectorArgs},
 Math.Vector2: {'__class__': JsonPickle.classNameFormatter,
                'args': JsonPickle.mathVectorArgs},
 tuple: {'__class__': JsonPickle.classNameFormatter,
         'args': lambda ob: [list(ob)]},
 set: {'__class__': JsonPickle.classNameFormatter,
       'args': lambda ob: [list(ob)]},
 long: {'__class__': JsonPickle.classNameFormatter,
        'args': lambda ob: [str(ob)]}}
MSGPACK_CLASSES_DECODER = dict([ (MSGPACK_CLASSES_ENCODER[cls]['__class__'](cls), cls) for cls in MSGPACK_CLASSES_ENCODER ])

class MsgPacker(msgpack.Packer):

    def pack_hook(self, obj, *args, **kwargs):
        cls = type(obj)
        if isinstance(obj, long) and obj < 18446744073709551616L:
            pass
        elif cls in MSGPACK_CLASSES_ENCODER:
            obj = dict([ (key, f(obj)) for key, f in MSGPACK_CLASSES_ENCODER.get(cls).items() ])
        return super(MsgPacker, self).pack_hook(obj, *args, **kwargs)


try:
    msgpack.Packer.pack_hook = msgpack.Packer._pack
    MsgPacker._pack = MsgPacker.pack_hook
except AttributeError:
    pass

def msgpackdumps(*args):
    return MsgPacker().pack(*args)


def msgpack_hook(obj):
    if '__class__' in obj:
        return MSGPACK_CLASSES_DECODER[obj['__class__']](*obj['args'], **obj.get('kw', {}))
    return obj


def msgpackloads(s, *args):
    if len(s) > MSGPACK_LOADS_MAX_STRING_SIZE:
        from debug_utils import LOG_DEBUG
        LOG_DEBUG('++++', len(s))
        raise MaxSizeLimit("MsgPack loads max size overhead. First 10 symbols '%s...'" % s[:10])
    return msgpack.loads(s, object_hook=msgpack_hook, *args)


def cpickledumps(*args):
    return cPickle.dumps(protocol=(-1), *args)


def jsonloads(s, *args):
    if len(s) > JSON_LOADS_MAX_STRING_SIZE:
        raise MaxSizeLimit("Json loads max size overhead. First 10 symbols '%s...'" % s[:10])
    return JsonPickle.loads(s, *args)


dumpHandlers = {FromClientToServer: msgpackdumps,
 FromClientToClient: cpickledumps,
 FromServerToServer: cpickledumps,
 FromServerToClient: cpickledumps,
 MsgPack: msgpackdumps}
loadHandlers = {FromClientToServer: msgpackloads,
 FromClientToClient: cPickle.loads,
 FromServerToServer: cPickle.loads,
 FromServerToClient: cPickle.loads,
 MsgPack: msgpackloads}

class WrongMessageFormat(Exception):
    pass


class MaxSizeLimit(Exception):
    pass


def profile(f):

    def _profile(*args, **kw):
        profileKey = next(args[f.func_code.co_varnames.index('profileKey'):].__iter__(), kw.get('profileKey', 'other'))
        t_before = time.time()
        r = f(*args, **kw)
        t_after = time.time()
        transferType = next(args[f.func_code.co_varnames.index('transferType'):].__iter__(), None)
        func_name = f.func_name
        size = len(r) if func_name == 'dumps' else len(next(args[1:].__iter__(), ''))
        log = PICKLER_LOG.setdefault(profileKey, {}).setdefault(transferType, {}).setdefault(f.func_name, {'average_time': 0.0,
         'runs_number': 0,
         'common_size': 0,
         'max_size': 0})
        runs_number = log['runs_number']
        average_time = log['average_time']
        log['average_time'] = (runs_number * average_time + t_after - t_before) / (runs_number + 1)
        log['runs_number'] = runs_number + 1
        log['common_size'] += size
        log['max_size'] = max(log['max_size'], size)
        return r

    if LOG_ENABLED:
        return _profile
    return f


def loads(transferType, s, profileKey = None, *args):
    match = MESSAGE_MATCHER.match(s)
    if match:
        groups = match.groups()
        s = zlib.decompress(groups[2]) if groups[1] == COMPRESS_PREFIX else groups[2]
        ob = loadHandlers[transferType](s, *args)
        return ob
    raise WrongMessageFormat("Wrong message format. First 10 symbols '%s...'" % s[:10])


def dumps(transferType, ob, profileKey = None, compress = True, *args):
    s = dumpHandlers[transferType](ob, *args)
    s = MESSAGE_FORMAT % ((COMPRESS_PREFIX, zlib.compress(s, COMPRESS_LEVEL)) if compress and AUTO_COMPRESS_LENGTH and len(s) > AUTO_COMPRESS_LENGTH else (PLAIN_PREFIX, s))
    return s


def profileOut(profileKey = None):
    if profileKey:
        return PICKLER_LOG.get(profileKey, None)
    else:
        return PICKLER_LOG


def profileClear(profileKey = None):
    if profileKey:
        if profileKey in PICKLER_LOG:
            del PICKLER_LOG[profileKey]
    else:
        PICKLER_LOG.clear()