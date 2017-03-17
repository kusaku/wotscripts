# Embedded file name: scripts/common/Operations/OperationBase.py
import Event
from debug_utils import LOG_DEBUG

class OperationBase:
    """
    Operation base
    """

    def __init__(self, operationCode, invocationId):
        """
        Constructor
        @param operationCode: operation code
        @param invocationId: invocation id
        """
        self._eventManager = Event.EventManager()
        self.onTimeout = Event.Event(self._eventManager)
        self.onDestroy = Event.Event(self._eventManager)
        self.__operationCode = operationCode
        self.__invocationId = invocationId
        self.__isDestroyed = False

    @property
    def operationCode(self):
        """
        Operation code getter
        @return: operation code
        @rtype: int
        """
        return self.__operationCode

    @property
    def invocationId(self):
        """
        Invocation id getter
        @return: invocation id
        @rtype: int
        """
        return self.__invocationId

    def destroy(self):
        """
        Destructor
        """
        if self.__isDestroyed:
            LOG_DEBUG('Attempt to destroy already destroyed operation')
            return
        else:
            self.onDestroy(self)
            self._eventManager.clear()
            self._eventManager = None
            self.onTimeout = None
            self.onDestroy = None
            self.__isDestroyed = True
            return