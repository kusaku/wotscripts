# Embedded file name: scripts/client/IfaceAPI.py
import inspect
from debug_utils import LOG_DEBUG
NO_RESULT = object()

class Promise(object):

    def __init__(self):
        super(Promise, self).__init__()
        self.__callback = None
        self.__result = NO_RESULT
        return

    def setCallback(self, callback):
        LOG_DEBUG('Promise::setCallback: {0}, {1}, {2}'.format(self, callback, self.__result))
        if self.__result is not NO_RESULT:
            callback(self.__result)
            return
        self.__callback = callback

    def callback(self, value):
        LOG_DEBUG('Promise::callback: {0}, {1}, {2}'.format(self, self.__callback, value))
        self.__result = value
        if callable(self.__callback):
            self.__callback(value)


class ReturnValueException(BaseException):

    def __init__(self, value):
        self.value = value


def async(func):
    if not inspect.isgeneratorfunction(func):
        raise Exception('async decorator used on non-generator function {0}'.format(func.__name__))

    def wrapper(*args, **kwargs):
        _gen = func(*args, **kwargs)
        promise = Promise()
        _async(_gen, promise, None)
        return promise

    return wrapper


def _async(gen, promise, result):
    try:
        result = gen.send(result)
    except (ReturnValueException, StopIteration) as e:
        value = getattr(e, 'value', None)
        promise.callback(value)
        return

    if isinstance(result, Promise):

        def onResult(r):
            _async(gen, promise, r)

        result.setCallback(onResult)
    return


def view(requestob):
    from gui.WindowsManager import g_windowsManager
    promise = Promise()
    LOG_DEBUG('View called: {0}, {1}'.format(requestob, promise))
    g_windowsManager.getAccountUI().viewIFace(requestob, dbgCallback=promise.callback)
    return promise


def _return(value):
    LOG_DEBUG('Async return, value: {0}'.format(value))
    raise ReturnValueException(value)