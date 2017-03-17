# Embedded file name: scripts/common/wofdecorators.py
from debug_utils import LOG_WRAPPED_CURRENT_EXCEPTION
import BigWorld

def noexcept(func):

    def wrapper(*args, **kwArgs):
        try:
            return func(*args, **kwArgs)
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)

    return wrapper


def nofail(func):

    def wrapper(*args, **kwArgs):
        try:
            return func(*args, **kwArgs)
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)
            import sys
            sys.exit()

    return wrapper


def timeLimit(skipTime):
    """
    wrap function for limit between calling
    """

    def decorator(func):

        def wrapper(*args, **kwArgs):
            callerId = args[0].id
            dt = BigWorld.time() - wrapper.callHistory.get(callerId, 0)
            if dt < wrapper.skipTime:
                return None
            else:
                wrapper.callHistory[callerId] = BigWorld.time()
                return func(*args, **kwArgs)

        wrapper.callHistory = {}
        wrapper.skipTime = skipTime
        return wrapper

    return decorator