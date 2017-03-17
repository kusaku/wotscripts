# Embedded file name: scripts/common/Operations/OperationSender.py
from Operations.SentOperation import SentOperation
from debug_utils import LOG_ERROR, LOG_OPERATION, LOG_TRACE
import wgPickle
from wofdecorators import noexcept
import threading
from config_consts import IS_DEVELOPMENT

class BACKUP_DATA_KEY:
    """
    backup data keys enum
    """
    INVOCATION_ID = 0
    OPERATION_CODE = 1
    TIMEOUT_NOTIFICATION = 2
    REMAINING_TIME = 3
    OPERATIONS = 4
    INVOCATION_COUNTER = 5


class Counter:
    """
    Counter class
    """

    def __init__(self):
        self.val = 0
        self.lock = threading.Lock()

    def inc(self):
        """
        Increase by one
        """
        self.val += 1


class OperationSender(object):
    """
    Operations sender. Could be used as base class.
    """

    def __init__(self, receiver, loadsTransferType, dumpsTransferType, invocationIdCounter = None):
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
        self.__receiver = receiver
        self.__operations = dict()
        self.__invocationIdCounter = invocationIdCounter or Counter()
        self.__loadsTransferType = loadsTransferType
        self.__dumpsTransferType = dumpsTransferType

    @property
    def receiver(self):
        """
        Operation receiver
        @return: operation receiver MAILBOX
        @rtype: MAILBOX
        """
        return self.__receiver

    @receiver.setter
    def receiver(self, receiver):
        """
        Sets receiver
        @param receiver:
        @type receiver: MAILBOX
        """
        self.__receiver = receiver

    def destroy(self):
        """
        Destructor
        """
        self.__receiver = None
        self.__invocationIdCounter = None
        for operation in self.__operations.values():
            operation.destroy()

        self.__operations.clear()
        self.__operations = None
        return

    @noexcept
    def backup(self):
        """
        Backup
        @return: backup data
        """
        operations = list()
        for operation in self.__operations.values():
            operations.append({BACKUP_DATA_KEY.INVOCATION_ID: operation.invocationId,
             BACKUP_DATA_KEY.OPERATION_CODE: operation.operationCode,
             BACKUP_DATA_KEY.TIMEOUT_NOTIFICATION: operation.timeoutClientNotification,
             BACKUP_DATA_KEY.REMAINING_TIME: operation.remainingTime})

        data = {BACKUP_DATA_KEY.OPERATIONS: operations,
         BACKUP_DATA_KEY.INVOCATION_COUNTER: self.__invocationIdCounter.val}
        return data

    @noexcept
    def restore(self, backupData):
        """
        Restore.
        NOTE: You should restore operation events delegates by your self
        @param backupData: backup data
        """
        self.__invocationIdCounter.val = backupData[BACKUP_DATA_KEY.INVOCATION_COUNTER]
        self.__operations = dict()
        for opData in backupData[BACKUP_DATA_KEY.OPERATIONS]:
            operation = SentOperation(self, opData[BACKUP_DATA_KEY.OPERATION_CODE], opData[BACKUP_DATA_KEY.INVOCATION_ID], opData[BACKUP_DATA_KEY.REMAINING_TIME], opData[BACKUP_DATA_KEY.TIMEOUT_NOTIFICATION])
            self.__operations[operation.invocationId] = operation
            operation.onDestroy += self.__onOperationDestroy
            operation.onTimeout += self.__onOperationTimeout

    def hasPendingOperation(self, invocationId):
        """
        Checks if there is a pending operation
        @param invocationId: invocation id
        @return: True if valid, otherwise - False
        """
        return self.__operations.has_key(invocationId)

    def unpackAgrumentString(self, argStr):
        """
        Unpacks arguments received with the response
        @param argStr: packed arguments
        @return: unpacked arguments
        @throws Exception: if there were any errors during unpack
        """
        try:
            return wgPickle.loads(self.__loadsTransferType, argStr)
        except Exception:
            LOG_ERROR('Unable to load incoming operation argStr: {0}'.format(argStr))
            raise

    def getOperationByInvocationId(self, invocationId):
        """
        Gets saved operation with specified invocation id
        @param invocationId: invocation id of the current operation
        @return: operation or None if operation does not exist
        """
        return self.__operations.get(invocationId, None)

    @noexcept
    def receiveOperationResponse(self, invocationId, returnCode, argStr):
        """
        Receives operation response
        @param invocationId: invocation id of the current operation
        @param returnCode: operation return code
        @param argStr: pickled arguments
        """
        args = self.unpackAgrumentString(argStr) if argStr else None
        operation = self.getOperationByInvocationId(invocationId)
        if not operation:
            LOG_ERROR('Received response with wrong invocation id', invocationId, args)
            if IS_DEVELOPMENT:
                from traceback import print_stack
                import StringIO
                f = StringIO.StringIO()
                print_stack(file=f)
                f.pos = 0
                LOG_ERROR(f.read())
            return
        else:
            operation._receiveResponse(returnCode, args)
            operation.destroy()
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
        operation = self._getNextOperation(operationCode, timeout, timeoutClientNotification)
        operationData = wgPickle.dumps(self.__dumpsTransferType, args)
        recipient.receiveOperation(operation.invocationId, operationCode, operationData)
        return operation

    def sendOperation(self, operationCode, timeout, timeoutClientNotification, *args):
        """
        Sends operation to recipient
        @param operationCode: operation code
        @param timeout: timeout value( should be > 0 to set timeout; <= 0 or None if no timeout)
        @param timeoutClientNotification:
        @param args: operation args
        @return: operation
        @rtype: SentOperation
        """
        return self.sendOperationTo(self.__receiver, operationCode, timeout, timeoutClientNotification, *args)

    def update(self, dt):
        for key, operation in self.__operations.items():
            operation.update(dt)

    def __onOperationTimeout(self, operation):
        if operation.timeoutClientNotification:
            self.__receiver.receiveOperationTimeout(operation.invocationId)
        operation.destroy()

    def __onOperationDestroy(self, operation):
        """
        
        @param operation:
        @type operation: SentOperation
        """
        LOG_OPERATION('Operation destroy:', operation.invocationId)
        del self.__operations[operation.invocationId]

    def _getNextOperation(self, operationCode, timeout, timeoutClientNotification):
        self.__invocationIdCounter.lock.acquire()
        operation = SentOperation(self, operationCode, self.__invocationIdCounter.val, timeout, timeoutClientNotification)
        self.__invocationIdCounter.inc()
        self.__invocationIdCounter.lock.release()
        operation.onDestroy += self.__onOperationDestroy
        operation.onTimeout += self.__onOperationTimeout
        self.__operations[operation.invocationId] = operation
        return operation