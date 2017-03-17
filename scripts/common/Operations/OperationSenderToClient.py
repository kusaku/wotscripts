# Embedded file name: scripts/common/Operations/OperationSenderToClient.py
from Operations.OperationSender import OperationSender, BACKUP_DATA_KEY, Counter
from Operations.SentOperation import SentOperation
from debug_utils import LOG_ERROR, LOG_DEBUG, CRITICAL_ERROR, LOG_CURRENT_EXCEPTION, LOG_OPERATION
import wgPickle
import zlib, cPickle
from wofdecorators import noexcept
from consts import STREAM_CLIENT, RESPONSE_TYPE

class OperationSenderToClient(OperationSender):
    """
    Operations sender. Could be used as base class.
    """

    def __init__(self, receiver, receiverBase, loadsTransferType, dumpsTransferType, invocationIdCounter = None):
        """
        Constructor
        @param receiver: operation receiver
        @type receiver: MAILBOX
        @type receiverBase: MAILBOX is used for streaming
        @param loadsTransferType: see wgPickle.py
            FromClientToServer
            FromClientToClient
            FromServerToServer
            FromServerToClient
        @param dumpsTransferType: see wgPickle.py
        @param invocationIdCounter: counter
        @type invocationIdCounter: Counter
        """
        OperationSender.__init__(self, receiver, loadsTransferType, dumpsTransferType, invocationIdCounter)
        if dumpsTransferType != wgPickle.FromServerToClient:
            CRITICAL_ERROR('OperationSenderToClient uses wrong dumpsTransferType.  ')
        self.__receiverBase = receiverBase

    def destroy(self):
        """
        Destructor
        """
        OperationSender.destroy(self)
        self.__receiverBase = None
        return

    def sendOperationTo(self, recipient, operationCode, timeout, timeoutClientNotification, *args):
        """
        Send operation to specific recipient
        @type recipient: MAILBOX
        @param operationCode:
        @param timeout:
        @param timeoutClientNotification:
        @param args:
        """
        if recipient is None:
            raise Exception, 'OperationSender::sendOperationTo: Trying to send operation to recipient which is None'
        if timeout is None or timeout <= 0:
            timeout = None
        operation = OperationSender._getNextOperation(self, operationCode, timeout, timeoutClientNotification)
        operationData = wgPickle.dumps(wgPickle.FromServerToClient, args)
        if self.__receiverBase:
            self.__receiverBase.toClientReceiveResponse(RESPONSE_TYPE.RESPONSE_TYPE_OPERATION, operation.invocationId, operationCode, operationData)
        else:
            if len(operationData) > STREAM_CLIENT.USE_PROXY_STREAM_FROM_SIZE:
                LOG_ERROR('Arguments is to log, define base for send by stream functionality op, size', operationCode, len(operationData))
            recipient.clientReceiveResponse(RESPONSE_TYPE.RESPONSE_TYPE_OPERATION, 0, operation.invocationId, operationCode, operationData)
        return operation