# Embedded file name: scripts/common/debug_utils.py
from itertools import imap
import sys
import types
from functools import wraps
from warnings import warn_explicit
import BigWorld
import os.path
import config_consts
from consts import IS_CHECK_REFERRERS, IS_CLIENT, ECONOMICS_ENABLE_LOG, BATTLE_ACTIVITY_POINTS_ENABLE_LOG, IS_BASEAPP
import gc
import pprint
import hotshot, hotshot.stats
import cProfile
import atexit
import inspect
import re

def CRITICAL_ERROR(msg, *kargs):
    msg = '{0}:{1}:{2}'.format(_makeMsgHeader(sys._getframe(1)), msg, kargs)
    if IS_CLIENT:
        BigWorld.terminate(msg)
    else:
        BigWorld.logError('PyException', msg)
        sys.exit()


TB_MAX_VARS_DEPTH = 1
TB_MAX_VARS_STR_LEN = 256

def myVarsPrint(lst, d = 0):
    res = {}
    for n, v in lst.items():
        if inspect.isclass(v) or inspect.ismodule(v):
            pass
        elif inspect.ismethod(v):
            res[n] = (type(v).__name__, '%s:%s' % (v.im_class.__name__, v.__name__))
        elif inspect.isfunction(v):
            res[n] = (type(v).__name__, '%s' % v.__name__)
        elif type(v) in [str,
         int,
         long,
         float,
         bool,
         set] or v in (None,):
            res[n] = (type(v).__name__, repr(v))
        elif type(v) in [list, tuple, dict]:
            if d > TB_MAX_VARS_DEPTH:
                res[n] = (type(v).__name__, '[Too deep]' if len(v) > 0 else repr(v))
                continue
            if type(v) == dict:
                k = v
            else:
                k = {}
                for i in range(len(v)):
                    k[i] = v[i]

            x = myVarsPrint(k, d + 1)
            res[n] = (type(v).__name__, x)
        elif type(v).__name__ == 'ResourceRefs':
            res[n] = (type(v).__name__, '[%s]' % type(v).__name__)
        else:
            if re.search(' at 0x[0-9A-Fa-f]{8}', repr(v)) is None:
                res[n] = (type(v).__name__, repr(v))
                continue
            if d > TB_MAX_VARS_DEPTH:
                res[n] = (type(v).__name__, '[Too deep]')
                continue
            k = myGetObjFields(v)
            res[n] = (type(v).__name__, myVarsPrint(k, d + 1))

    return res


def myGetObjFields(o):
    f = {}
    for k in dir(o):
        if '__' not in (k[:2], k[-2:]) and hasattr(o, k) and not inspect.isclass(o):
            v = getattr(o, k)
            if not type(v).__name__.endswith('method'):
                f[k] = v

    return f


def dumpTBVars(tb):
    if IS_CLIENT:
        print 'traceback vars:'
        while tb:
            fr = tb.tb_frame
            if tb.tb_next is None:
                res = str(myVarsPrint(fr.f_locals))
                while res:
                    res1, res = res[:TB_MAX_VARS_STR_LEN], res[TB_MAX_VARS_STR_LEN:]
                    BigWorld.logError('TB:PyException', res1)

            tb = tb.tb_next

    return


def LOG_CURRENT_EXCEPTION():
    BigWorld.logError('PyException', _makeMsgHeader(sys._getframe(1)))
    exctype, value = sys.exc_info()[:2]
    sys.excepthook(exctype, value, sys.exc_traceback)


def LOG_WRAPPED_CURRENT_EXCEPTION(wrapperName, orgName, orgSource, orgLineno):
    print '[%s] (%s, %d):' % ('EXCEPTION', orgSource, orgLineno)
    from sys import exc_info
    from traceback import format_tb, format_exception_only
    etype, value, tb = exc_info()
    if tb:
        list = ['Traceback (most recent call last):\n']
        list = list + format_tb(tb)
    else:
        list = []
    list = list
    for ln in list:
        if ln.find(wrapperName) == -1:
            sys.stderr.write(ln)

    list = format_exception_only(etype, value)
    for ln in list:
        sys.stderr.write(ln.replace(wrapperName, orgName))


def LOG_CODEPOINT_WARNING(*kargs):
    _doLog('WARNING', 'see the source code for details', *kargs)


def LOG_ERROR(msg, *args, **kwargs):
    from config_consts import IS_QA_TESTING
    if IS_QA_TESTING and kwargs.pop('IS_QA_TESTING', True):
        import traceback
        traceback.print_stack()
    _doLog('ERROR', msg, *args)


def LOG_WARNING(msg, *kargs):
    _doLog('WARNING', msg, *kargs)


def LOG_WARNING_DEBUG(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('WARNING', msg, *kargs)


def LOG_TRACE(msg, *kargs):
    _doLog('TRACE', msg, *kargs)


def LOG_TRACE_DEV(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('TRACE', msg, *kargs)


def LOG_INFO(msg, *kargs):
    _doLog('INFO', msg, *kargs)


def LOG_NOTE(msg, *kargs):
    _doLog('NOTE', msg, *kargs)


def LOG_DEBUG(msg, *kargs):
    if config_consts.IS_DEVELOPMENT or not IS_CLIENT:
        _doLog('DEBUG', msg, *kargs)


def LOG_DEBUG_DEV(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('DEBUG', msg, *kargs)


def LOG_NESTE(msg, *kargs):
    if config_consts.IS_DEVELOPMENT or not IS_CLIENT:
        _doLog('NESTE', msg, *kargs)


def LOG_MX(msg, *kargs):
    if config_consts.IS_DEVELOPMENT or not IS_CLIENT:
        _doLog('MX', msg, *kargs)


def LOG_MX_DEV(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('MX', msg, *kargs)


def LOG_DZ(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('DZ', msg, *kargs)


def LOG_RF(msg, *kargs):
    if config_consts.IS_DEVELOPMENT or not IS_CLIENT:
        _doLog('RF', msg, *kargs)


def LOG_UNEXPECTED(msg, *kargs):
    _doLog('LOG_UNEXPECTED', msg, *kargs)


def LOG_WRONG_CLIENT(entity, *kargs):
    if hasattr(entity, 'id'):
        entity = '[%s, %s]' % (str(entity.id), str(getattr(entity, 'databaseID', '')))
    BigWorld.logError('WRONG_CLIENT', ' '.join(map(str, [_makeMsgHeader(sys._getframe(1)), entity, kargs])))


def LOG_OPERATION(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('OPERATION:', msg, *kargs)


DATABASE_HASHTAG = '#Db'

def DBLOG_ERROR(msg, *kargs):
    """Print tagged log message, error"""
    _doLog('ERROR_DB', (DATABASE_HASHTAG + ' ' + msg), *kargs)


def DBLOG_NOTE(msg):
    """Print tagged log message, note"""
    if config_consts.DB_ENABLE_LOG and config_consts.IS_DEVELOPMENT:
        LOG_DEBUG(DATABASE_HASHTAG + ' ' + msg)


def DBLOG_CRITICAL(msg):
    """Print tagged log message, critival error"""
    CRITICAL_ERROR(DATABASE_HASHTAG + ' ' + msg)


def ECONOMICS_LOG_NOTE(msg, *kargs):
    """Print tagged log message, note"""
    if ECONOMICS_ENABLE_LOG and config_consts.IS_DEVELOPMENT:
        _doLog('NOTE', ('[ECONOMICS] %s' % msg), *kargs)


def ECONOMICS_LOG_DICT(title, data):
    """
    Log dict data to Economics Log
    :type data: dict
    :type title: basestring
    :param title: title of dict
    :param data: dict to print
    """
    import json
    if ECONOMICS_ENABLE_LOG and config_consts.IS_DEVELOPMENT:
        ECONOMICS_LOG_NOTE(title)
        if data:
            s = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')).split('\n')
            for ss in s:
                ECONOMICS_LOG_NOTE(ss)


def BATTLE_ACTIVITY_LOG_NOTE(msg, *kargs):
    """Print tagged log message, note"""
    if BATTLE_ACTIVITY_POINTS_ENABLE_LOG:
        _doLog('NOTE', ('[BATTLE ACTIVITY] %s' % msg), *kargs)


def LOG_TU(msg, *kargs):
    if config_consts.IS_DEVELOPMENT:
        _doLog('TU', msg, *kargs)


def _logFormat(entity, formatStr, *args, **kwargs):
    try:
        if args or kwargs:
            formatStr = formatStr.format(*args, **kwargs)
        if entity is None:
            return formatStr
        return '[%s, %s, %s] %s ' % (entity.__class__.__name__,
         str(entity.id),
         str(getattr(entity, 'databaseID', '')),
         formatStr)
    except:
        print 'Bad args format or encoding! Fix incoming data', formatStr, args, kwargs
        import traceback
        traceback.print_stack()
        return ''

    return


def LOG_ERROR_FORMAT(entity, formatStr, *args, **kwargs):
    """
    @param entity: entity or Base instance
    @param formatStr: format string (example 'Invalid param = {0}')
    @param args: format string args
    @param kwargs: format string kwargs
    """
    from config_consts import IS_QA_TESTING
    if IS_QA_TESTING and kwargs.pop('IS_QA_TESTING', True):
        import traceback
        traceback.print_stack()
    _doLog('ERROR', _logFormat(entity, formatStr, *args, **kwargs))


def LOG_INFO_FORMAT(entity, formatStr, *args, **kwargs):
    """
    
    @param entity: entity or Base instance
    @param formatStr: format string (example 'Invalid param = {0}')
    @param args: format string args
    @param kwargs: format string kwargs
    """
    _doLog('INFO', _logFormat(entity, formatStr, *args, **kwargs))


def LOG_DEBUG_FORMAT(entity, formatStr, *args, **kwargs):
    """
    @param entity: entity or Base instance
    @param formatStr: format string (example 'Invalid param = {0}')
    @param args: format string args
    @param kwargs: format string kwargs
    """
    if config_consts.IS_DEVELOPMENT or not IS_CLIENT:
        _doLog('DEBUG', _logFormat(entity, formatStr, *args, **kwargs))


def LOG_WARNING_FORMAT(entity, formatStr, *args, **kwargs):
    """
    @param entity: Entity or Base instance
    @param formatStr: format string (example 'Invalid param = {0}')
    @param args: format string args
    @param kwargs: format string kwargs
    """
    _doLog('WARNING', _logFormat(entity, formatStr, *args, **kwargs))


def LOG_NOTE_FORMAT(entity, formatStr, *args, **kwargs):
    """
    @param entity: Entity or Base instance
    @param formatStr: format string (example 'Invalid param = {0}')
    @param args: format string args
    @param kwargs:
    """
    _doLog('NOTE', _logFormat(entity, formatStr, *args, **kwargs))


def LOG_EXCHANGE_API(entity, formatStr, ifaceStr):
    if not IS_BASEAPP:
        return
    if not BigWorld.baseAppData['exchangeApiEnableLog']:
        ifaceStr = [ifaceStr[0], ifaceStr[2]]
    if config_consts.IS_DEVELOPMENT or not IS_CLIENT:
        _doLog('DEBUG', _logFormat(entity, '%s: %s' % (str(formatStr), str(ifaceStr))))


def MQ_LOG_DEBUG(msg, *args, **kwargs):
    if config_consts.MQ_ENABLE_LOG:
        _doLog('DEBUG', ('[MQ] %s' % msg), *args)
        for k in pprint.pformat(kwargs).split('\n'):
            _doLog('DEBUG', '[MQ]   %s' % str(k))


def DATA_STRUCTURE_LOG_DEBUG(msg, struct):
    if config_consts.IS_DEVELOPMENT:
        _doLog('DEBUG', '[STRUCT] %s' % msg)
        for k in pprint.pformat(struct).split('\n'):
            _doLog('DEBUG', '[STRUCT]   %s' % str(k))


def LOG_TRANSACTION(entity, transactionID, transactionData, isVirtual, fromClient):
    prefix = '{vFlag}trid'.format(vFlag=isVirtual and 'v' or '')
    extTransactionID = '{0}{sFlag}'.format(transactionID, sFlag=not fromClient and 's' or '')
    _doLog('DEBUG', _logFormat(entity, '{0}:{1}:{2}', prefix, extTransactionID, transactionData))


logMapping = {'TRACE': BigWorld.logTrace,
 'DEBUG': BigWorld.logDebug,
 'INFO': BigWorld.logInfo,
 'NOTE': BigWorld.logNotice,
 'NOTICE': BigWorld.logNotice,
 'WARNING': BigWorld.logWarning,
 'ERROR': BigWorld.logError,
 'CRITICAL': BigWorld.logCritical,
 'HACK': BigWorld.logHack}

def _doLog(s, msg, *args):
    header = _makeMsgHeader(sys._getframe(2))
    logFunc = logMapping.get(s, None)
    category = 'SCRIPT'
    if not logFunc:
        category = '%s %s' % (category, s)
        logFunc = BigWorld.logInfo
    if args:
        output = ' '.join(map(str, [header, msg, args]))
    else:
        output = ' '.join(map(str, [header, msg]))
    logFunc(category, output)
    return


def _makeMsgHeader(frame):
    return '(%s, %d):' % (frame.f_code.co_filename, frame.f_lineno)


def trace(func):
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    frame = sys._getframe(1)

    @wraps(func)
    def wrapper(*args, **kwds):
        entID = ' [id=%s]' % str(args[0].id) if len(args) > 0 and hasattr(args[0], 'id') else ''
        BigWorld.logDebug(' '.join('(%s, %d)%s call %s:' % (frame.f_code.co_filename,
         frame.f_lineno,
         entID,
         fname), ':', ', '.join(('%s=%r' % entry for entry in zip(argnames, args) + kwds.items()))))
        ret = func(*args, **kwds)
        BigWorld.logDebug(' '.join('(%s, %d)%s return from %s:' % (frame.f_code.co_filename,
         frame.f_lineno,
         entID,
         fname), ':', repr(ret)))
        return ret

    return wrapper


def deprecated(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        warn_explicit('Call to deprecated function %(funcname)s.' % {'funcname': func.__name__}, category=DeprecationWarning, filename=func.func_code.co_filename, lineno=func.func_code.co_firstlineno + 1)
        return func(*args, **kwargs)

    return wrapper


def disabled(func):

    def empty_func(*args, **kargs):
        pass

    return empty_func


def dump_garbage(source = False):
    """
    show us what's the garbage about
    """
    import inspect, gc
    print '\nCollecting GARBAGE:'
    gc.collect()
    print '\nCollecting GARBAGE:'
    gc.collect()
    print '\nGARBAGE OBJECTS:'
    for x in gc.garbage:
        try:
            s = str(x)
            if len(s) > 80:
                s = '%s...' % s[:80]
            print '::', s
            print '        type:', type(x)
            print '   referrers:', len(gc.get_referrers(x))
            print '    is class:', inspect.isclass(type(x))
            print '      module:', inspect.getmodule(x)
            if source:
                lines, line_num = inspect.getsourcelines(type(x))
                print '    line num:', line_num
                for l in lines:
                    print '        line:', l.rstrip('\n')

        except:
            pass


def dump_mem_leaks():
    gc.collect()
    if len(gc.garbage) > 0:
        print 'Leaks detected:'
        for obj in filter(lambda x: type(x).__name__ == 'instance', gc.garbage):
            print '%10d %s' % (sys.getrefcount(obj), obj)


def dump_mem_leaks_all():
    gc.collect()
    if len(gc.garbage) > 0:
        LOG_ERROR('Leaks detected: %d' % len(gc.garbage))
        if config_consts.IS_DEVELOPMENT:
            fname = os.path.join(BigWorld.getUserDataDirectory(), 'logs/', 'py_leaks.txt')
            with open(fname, 'w') as f:
                pp = pprint.PrettyPrinter(indent=4, width=80, depth=None, stream=f)
                pp.pprint(gc.garbage)
    return


def get_refcounts():
    d = {}
    sys.modules
    for m in sys.modules.values():
        for sym in dir(m):
            o = getattr(m, sym)
            if type(o) is types.ClassType:
                d[o] = sys.getrefcount(o)

    pairs = map(lambda x: (x[1], x[0]), d.items())
    pairs.sort()
    pairs.reverse()
    return pairs


def print_refs_top_100():
    for n, c in get_refcounts()[:100]:
        print '%10d %s' % (n, c.__name__)


def dump_all():
    fname = os.path.join(os.getcwd(), 'all_python.txt')
    with open(fname, 'w') as f:
        pp = pprint.PrettyPrinter(indent=4, width=80, depth=None, stream=f)
        pp.pprint(gc.get_objects())
    return


def dump_refs(obj, file_name):
    fname = os.path.join(os.getcwd(), file_name)
    with open(fname, 'w') as f:
        pp = pprint.PrettyPrinter(indent=4, width=80, depth=None, stream=f)
        pp.pprint(obj)
        pp.pprint(gc.get_referrers(obj))
    return


def verify(expression):
    try:
        raise expression or AssertionError
    except AssertionError:
        LOG_CURRENT_EXCEPTION()


def stressCreateTexture(num):
    resList = [1024, 2048]
    textures = []
    valid = True
    while valid and num > 0:
        for res in resList:
            tex = BigWorld.createTexture(res, res)
            textures.append(tex)
            if tex == 0:
                valid = False
                break

        smallIdx = len(textures) - 2
        BigWorld.deleteTexture(textures.pop(smallIdx))
        num -= 1


def hotshotProfile(numResults, func, *args, **kw):
    prof = hotshot.Profile('hotshot.prof')
    prof.runcall(func, *args, **kw)
    prof.close()
    stats = hotshot.stats.load('hotshot.prof')
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats(numResults)


def print_cycles(objects, outstream = sys.stdout, show_progress = False):
    """
    objects:       A list of objects to find cycles in.  It is often useful
                   to pass in gc.garbage to find the cycles that are
                   preventing some objects from being garbage collected.
    outstream:     The stream for output.
    show_progress: If True, print the number of objects reached as they are
                   found.
    """
    from types import FrameType

    def print_path(path):
        for i, step in enumerate(path):
            next = path[(i + 1) % len(path)]
            outstream.write('   %s -- ' % str(type(step)))
            if isinstance(step, dict):
                for key, val in step.items():
                    if val is next:
                        outstream.write('[%s]' % repr(key))
                        break
                    if key is next:
                        outstream.write('[key] = %s' % repr(val))
                        break

            elif isinstance(step, list):
                outstream.write('[%d]' % step.index(next))
            elif isinstance(step, tuple):
                outstream.write('[%d]' % list(step).index(next))
            else:
                outstream.write(repr(step))
            outstream.write(' ->\n')

        outstream.write('\n')

    def recurse(obj, start, all, current_path):
        if show_progress:
            outstream.write('%d\r' % len(all))
        all[id(obj)] = None
        referents = gc.get_referents(obj)
        for referent in referents:
            if referent is start:
                print_path(current_path)
            elif referent is objects or isinstance(referent, FrameType):
                continue
            elif id(referent) not in all:
                recurse(referent, start, all, current_path + [obj])

        return

    for obj in objects:
        outstream.write('Examining: %r\n' % obj)
        recurse(obj, obj, {}, [])


def referrers_check(func):
    """
    DECORATOR.
    Checks the referrers of the owner of current func.
    Use only with class non static methods.
    @param func:
    """
    if not IS_CHECK_REFERRERS:
        return func

    def _referrers_check_decorator_flag(self, *args, **kvargs):
        g = globals()
        if g.get('_referrers_check_decorator_flag', False):
            return func(self, *args, **kvargs)

        def __hasInst(referrer, clazz):
            if isinstance(referrer, clazz):
                return True
            if isinstance(referrer, dict):
                for re in referrer.itervalues():
                    if __hasInst(re, clazz):
                        return True

        g['_referrers_check_decorator_flag'] = True
        res = func(self, *args, **kvargs)
        g['_referrers_check_decorator_flag'] = False
        referrers = [ r for r in gc.get_referrers(self) if __hasInst(r, self.__class__) ]
        if referrers:
            LOG_ERROR('----------------------------------------------')
            LOG_ERROR('Referrers of instance of class {0}:'.format(self.__class__.__name__))
            for r in referrers:
                data = str(r)
                max_size = 1500
                if len(data) < max_size:
                    LOG_ERROR('->{0}: {1}'.format(type(r).__name__, r))
                else:
                    LOG_ERROR('->{0}: '.format(type(r).__name__))
                    for chunk_start in xrange(0, len(data), max_size):
                        LOG_ERROR('    {0}'.format(data[chunk_start:chunk_start + max_size]))

            LOG_ERROR('----------------------------------------------')
            raise Exception('Found instance referrers({0}) of instance of class {1}'.format(len(referrers), self.__class__.__name__))
        return res

    return _referrers_check_decorator_flag


def profile(fn):
    return fn


if config_consts.IS_DEVELOPMENT and IS_CLIENT:
    g_profiler = cProfile.Profile()

    def shutdownProfiler():
        global g_profiler
        fname = os.path.join(BigWorld.getUserDataDirectory(), 'logs/', 'py_profile.pstats')
        g_profiler.dump_stats(fname)
        g_profiler = None
        return


    atexit.register(shutdownProfiler)

    def profileImpl(fn):

        def decorated(*args, **kwargs):
            g_profiler.enable()
            result = fn(*args, **kwargs)
            g_profiler.disable()
            return result

        return decorated


    profile = profileImpl

def _logmethod(method):

    def _method(self, *argl, **argd):
        args = []
        for id, item in enumerate(argl):
            args.append('%s=%s' % (method.func_code.co_varnames[id + 1], str(item)))

        for key, item in argd.items():
            args.append('%s=%s' % (key, str(item)))

        argstr = ','.join(args)
        print 'CALL %s.%s(%s) ' % (self.__class__.__name__, method.func_name, argstr)
        returnval = getattr(self, '_H_%s' % method.func_name)(*argl, **argd)
        return returnval

    return _method


class LogTheMethods(type):
    """meta class for loging all methods calling"""

    def __new__(cls, classname, bases, classdict):
        logmatch = re.compile(classdict.get('logMatch', '(?!_).*'))
        for attr, item in classdict.items():
            if callable(item) and logmatch.match(attr):
                classdict['_H_%s' % attr] = item
                classdict[attr] = _logmethod(item)

        return type.__new__(cls, classname, bases, classdict)


def startObserv(obj):
    pass


def endObserv(obj):
    pass


def IfaceDebugOutput(commandType, **kwargs):
    pass


class TempMessage:
    lbl = None
    cb = -1

    def __init__(self, txt, time = 5.0, color = (0, 255, 0, 255)):
        import GUI
        if TempMessage.lbl is not None:
            TempMessage.__clear()
        TempMessage.lbl = GUI.Text(txt)
        TempMessage.lbl.horizontalPositionMode = 'CLIP'
        TempMessage.lbl.verticalPositionMode = 'CLIP'
        TempMessage.lbl.horizontalAnchor = 'LEFT'
        TempMessage.lbl.verticalAnchor = 'TOP'
        TempMessage.lbl.position = (-1, 0.5, 0)
        TempMessage.lbl.multiline = True
        TempMessage.lbl.colour = color
        TempMessage.lbl.font = 'system_large.font'
        GUI.addRoot(TempMessage.lbl)
        TempMessage.cb = BigWorld.callback(time, TempMessage.__clear)
        return

    @staticmethod
    def __clear():
        import GUI
        GUI.delRoot(TempMessage.lbl)
        TempMessage.lbl = None
        BigWorld.cancelCallback(TempMessage.cb)
        TempMessage.cb = -1
        return


def initDebug(configSection):
    if not configSection:
        return
    import ResMgr
    import importlib
    if configSection['pythonpath']:
        for path in [ p.asString for p in configSection['pythonpath'].values() ]:
            fullPath = ResMgr.resolveToAbsolutePath(path)
            if fullPath not in sys.path:
                sys.path.append(fullPath)

    if configSection['ipc']:
        try:
            from testcore import bwreactor
            bwreactor.install()
            from testcore.ipc import peers
            peerName = configSection['ipc']['peer'].asString
            peer = importlib.import_module('.' + peerName, 'testcore.ipc.peers')
        except (ImportError, AttributeError) as e:
            LOG_ERROR("Can't load ipc peer: %s" % e)
        else:
            timeout = configSection['ipc'].readInt('timeout', 0)
            peer.init(BigWorld.component, timeout)