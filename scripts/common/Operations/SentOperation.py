# Embedded file name: scripts/common/Operations/SentOperation.py
import Event
from Operations.OperationBase import OperationBase

class SentOperation(OperationBase):
    """
    Operation on sender side
    """

    def __init__(self, sender, operationCode, invocationId, time, timeoutClientNotification = True):
        """
        Constructor
        @param sender: operation sender
        @type sender: OperationSender
        @param operationCode: operation code
        @param invocationId:
        @param time:
        @param timeoutClientNotification:
        """
        OperationBase.__init__(self, operationCode, invocationId)
        self.onResponse = Event.Event(self._eventManager)
        self.timeoutClientNotification = timeoutClientNotification
        self.__remainingTime = time
        self.__sender = sender

    @property
    def sender(self):
        """
        Operation sender
        @rtype: OperationSender
        """
        return self.__sender

    @property
    def remainingTime(self):
        return self.__remainingTime

    def update(self, dt):
        if self.__remainingTime is not None:
            self.__remainingTime -= dt
            if self.__remainingTime <= 0:
                self.__remainingTime = None
                self.onTimeout(self)
        return

    def destroy(self):
        """
        Destructor
        """
        self.onResponse.clear()
        self.onResponse = None
        self.__sender = None
        OperationBase.destroy(self)
        return

    def _receiveResponse(self, returnCode, args):
        """
        Receive response.
        @param returnCode: operation return code
        @type returnCode: int
        @param args: response arguments
        @type args: list
        """
        if args:
            self.onResponse(self, returnCode, *args)
        else:
            self.onResponse(self, returnCode)