# Embedded file name: scripts/common/Operations/ReceivedOperation.py
from Operations.OperationBase import OperationBase
from debug_utils import LOG_ERROR

class ReceivedOperation(OperationBase):
    """
    Operation on receiver side
    """

    def __init__(self, mgr, operationCode, invocationId, args = None):
        """
        Constructor
        @param mgr:
        @type mgr: OperationReceiverBase
        @param operationCode:
        @param invocationId:
        @param args: list with arguments
        @type args: list
        """
        OperationBase.__init__(self, operationCode, invocationId)
        self.__mgr = mgr
        self.__args = args

    @property
    def receiver(self):
        """
        @rtype: OperationReceiverBase
        """
        return self.__mgr

    def destroy(self):
        """
        Release the resources
        """
        self.__mgr = None
        self.__args = None
        OperationBase.destroy(self)
        return

    @property
    def args(self):
        """
        Operation arguments getter
        @return: arguments or None
        @rtype: list
        """
        return self.__args

    def sendResponse(self, returnCode, *args):
        """
        Send operation response and destroy
        @param returnCode: operation return code
        @type returnCode: int
        @param args: response arguments
        """
        if self.__mgr is None:
            LOG_ERROR('ReceivedOperation:sendResponse. Try to double send same operation. Operation Code: %d' % self.invocationId)
            return
        else:
            self.__mgr._sendOperationResponse(self, returnCode, *args)
            self.destroy()
            return

    def receiveTimeout(self):
        """
        Dispatches timeout event and destroys
        """
        self.onTimeout(self)
        self.destroy()