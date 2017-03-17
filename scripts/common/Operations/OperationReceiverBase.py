# Embedded file name: scripts/common/Operations/OperationReceiverBase.py
from abc import ABCMeta, abstractmethod
import cPickle
import zlib
from Event import Event
from Operations.ReceivedOperation import ReceivedOperation
from consts import STREAM_CLIENT, RESPONSE_TYPE
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG_DEV
import wgPickle
from wofdecorators import noexcept

class BACKUP_DATA_KEY:
    """
    backup data keys enum
    """
    INVOCATION_ID = 0
    OPERATION_CODE = 1
    ARGS = 2


class OperationReceiverBase(object):
    """
    Base class for operations recipient
    """
    __metaclass__ = ABCMeta

    def __init__(self, sender, loadsTransferType, dumpsTransferType, streamer = None):
        """
        Constructor
        @param sender: operation sender
        @type sender: MAILBOX
        @param loadsTransferType: see wgPickle.py
        @param dumpsTransferType: see wgPickle.py
        @param streamer:
        @type streamer: BigWorld.Proxy
        """
        self._sender = sender
        self.__streamer = streamer
        self.__operations = dict()
        self.__loadsTransferType = loadsTransferType
        self.__dumpsTransferType = dumpsTransferType
        self.onOperationRestoredEvent = Event()

    @property
    def sender(self):
        """
        Operation sender
        @rtype: MAILBOX
        """
        return self._sender

    @property
    def operations(self):
        """
        Received operations
        @return: dict of operations
        @rtype: dict
        """
        return self.__operations

    def destroy(self):
        """
        Destructor
        """
        self._sender = None
        self.clearOperations()
        self.__operations = None
        self.__streamer = None
        self.onOperationRestoredEvent.clear()
        self.onOperationRestoredEvent = None
        return

    @noexcept
    def backup(self):
        """
        Backup
        @return: backup data
        """
        data = list()
        for operation in self.__operations.values():
            opData = {BACKUP_DATA_KEY.INVOCATION_ID: operation.invocationId,
             BACKUP_DATA_KEY.OPERATION_CODE: operation.operationCode}
            if operation.args:
                opData[BACKUP_DATA_KEY.ARGS] = operation.args
            data.append(opData)

        return data

    @noexcept
    def restore(self, backupData):
        """
        Restore
        @param backupData: backup data
        """
        for operationData in backupData:
            operation = ReceivedOperation(self, operationData[BACKUP_DATA_KEY.OPERATION_CODE], operationData[BACKUP_DATA_KEY.INVOCATION_ID], operationData.get(BACKUP_DATA_KEY.ARGS, None))
            operation.onDestroy += self.__onOperationDestroy
            self.__operations[operation.invocationId] = operation
            self.onOperationRestoredEvent(operation)

        return

    @noexcept
    def receiveOperationTimeout(self, invocationId):
        """
        Receives timeout for specific operation
        @param invocationId: invocation id of the received operation
        """
        operation = self.__operations.get(invocationId, None)
        if operation is not None:
            operation.receiveTimeout()
        else:
            LOG_ERROR('Received timeout notification for not existing operation (invocationId = {0})'.format(invocationId))
        return

    @noexcept
    def receiveOperation(self, invocationId, operationCode, argStr):
        """
        Receives operation
        @param operationCode: operation code
        @param invocationId: invocation id of the received operation, need for response
        @param argStr: pickled operation arguments
        """
        if self.__operations.has_key(invocationId):
            LOG_ERROR('Received duplicate invocation id ({0} {1})'.format(invocationId, self.__operations[invocationId].__dict__))
            self.__operations[invocationId].destroy()
        args = None
        if argStr:
            try:
                args = wgPickle.loads(self.__loadsTransferType, argStr)
                if not isinstance(args, tuple):
                    LOG_ERROR('Incoming operation args are corrupted (not a tuple)')
                    return
            except Exception:
                LOG_ERROR('Unable to load incoming operation argStr')
                return

        operation = ReceivedOperation(self, operationCode, invocationId, args)
        operation.onDestroy += self.__onOperationDestroy
        self.__operations[operation.invocationId] = operation
        self._onReceiveOperation(operation)
        return

    def _sendOperationResponse(self, operation, returnCode, *args):
        """
        @type operation: ReceivedOperation
        @param returnCode:
        @param args:
        """
        responseData = wgPickle.dumps(self.__dumpsTransferType, args)
        if self.__streamer:
            self.__streamer.toClientReceiveResponse(RESPONSE_TYPE.RESPONSE_TYPE_CMD, operation.invocationId, returnCode, responseData)
        else:
            self._sender.receiveOperationResponse(operation.invocationId, returnCode, responseData)

    @abstractmethod
    def _onReceiveOperation(self, operation):
        """
        Override to implement reaction on operations
        @param operation: received operation
        @type operation: ReceivedOperation
        """
        pass

    def __onOperationDestroy(self, operation):
        del self.__operations[operation.invocationId]

    def clearOperations(self):
        for operation in self.__operations.values():
            operation.onDestroy.clear()
            operation.destroy()

        self.__operations.clear()
        LOG_DEBUG_DEV('clearOperations successed')