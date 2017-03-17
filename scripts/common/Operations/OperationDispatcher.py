# Embedded file name: scripts/common/Operations/OperationDispatcher.py
from Operations.OperationReceiverBase import OperationReceiverBase
from debug_utils import LOG_WARNING, LOG_DEBUG

class OperationHandlerBase:

    def __init__(self, handlers):
        """
        @param handlers: dict where key - operation code, value - delegate handler
        @return:
        """
        self.__handlers = handlers

    def handle(self, operation):
        """
        Handle operation
        @type operation: ReceivedOperation
        """
        handler = self.__handlers.get(operation.operationCode, None)
        if handler:
            handler(operation)
            return True
        else:
            return False

    def destroy(self):
        self.__handlers = None
        return


class OperationDispatcher(OperationReceiverBase):
    """
    Operation receiver that delegates operation handling to handlers
    """

    def __init__(self, sender, loadsTransferType, dumpsTransferType, streamer, *handlers):
        """
        
        @param sender:
        @type handlers: OperationHandlerBase
        """
        OperationReceiverBase.__init__(self, sender, loadsTransferType, dumpsTransferType, streamer)
        self.handlers = list(handlers)

    def _onReceiveOperation(self, operation):
        for handler in self.handlers:
            if handler.handle(operation):
                return

        LOG_WARNING('Received unhandled operation (code = {0})'.format(operation.operationCode))

    def destroy(self):
        for handler in self.handlers:
            handler.destroy()

        self.handlers = None
        OperationReceiverBase.destroy(self)
        return