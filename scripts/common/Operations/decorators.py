# Embedded file name: scripts/common/Operations/decorators.py
from debug_utils import LOG_WRONG_CLIENT

def operationRequestHandler(*argsTypes):
    """
    Server only. Decorator for server operation handlers.
    @param argsTypes: list of expected types of operation arguments
    @return:
    """

    def decorator(func):

        def wrapper(self, operation):
            """
            @type self:
            @type operation: ReceivedOperation
            """
            if len(operation.args) != len(argsTypes):
                LOG_WRONG_CLIENT(operation.receiver.sender, '[REQUEST] Inconsistent operation args count. Expected {0}, got {1}. Operation code = {2}'.format(len(argsTypes), len(operation.args), operation.operationCode), func.__name__)
                return
            for i, t in enumerate(argsTypes):
                if not isinstance(operation.args[i], t):
                    LOG_WRONG_CLIENT(operation.receiver.sender, '[REQUEST] Inconsistent operation argument[{0}] type. Expected {1}, got {2}. Operation code = {3}'.format(i, t, type(operation.args[i]), operation.operationCode), func.__name__)
                    return

            func(self, operation)

        return wrapper

    return decorator


def operationResponseHandler(*argsTypes):
    """
    Server only. Decorator for server operation response handlers.
    @param argsTypes: list of expected types of operation response arguments
    @return:
    """

    def decorator(func):

        def wrapper(self, operation, returnCode, *args):
            """
            @type self:
            @type operation: SentOperation
            @param returnCode:
            @param args:
            """
            if len(args) != len(argsTypes):
                LOG_WRONG_CLIENT(operation.sender.receiver, '[RESPONSE] Inconsistent operation args count. Expected {0}, got {1}. Operation code = {2}'.format(len(args), len(argsTypes), operation.operationCode), func.__name__)
                return
            for i, t in enumerate(argsTypes):
                if not isinstance(args[i], t):
                    LOG_WRONG_CLIENT(operation.sender.receiver, '[RESPONSE] Inconsistent operation argument[{0}] type. Expected {1}, got {2}. Operation code = {3}'.format(i, t, type(args[i]), operation.operationCode), func.__name__)
                    return

            func(self, operation, returnCode, *args)

        return wrapper

    return decorator