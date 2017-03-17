# Embedded file name: scripts/common/TutorialCommon/TriggerBase.py
from abc import ABCMeta, abstractmethod
from Event import Event

class TriggerBase(object):
    """
    Abstract class
    Trigger base class
    """
    __metaclass__ = ABCMeta

    def __init__(self, data, operation):
        """
        Constructor
        @param data: trigger data
        @param operation: trigger operation
        @type operation: ReceivedOperation
        """
        self.onStateChanged = Event()
        self.onFailed = Event()
        self.data = data
        self.operation = operation
        self._initialized = False
        self._isConditionsComplete = False

    def destroy(self):
        """
        Destructor
        """
        self.onStateChanged.clear()
        self.onStateChanged = None
        self.onFailed.clear()
        self.onFailed = None
        self.operation = None
        self.data = None
        self._initialized = False
        self._isConditionsComplete = False
        return

    @abstractmethod
    def update(self, dt):
        """
        Update trigger state
        @param dt: delta time
        """
        pass

    def initialize(self):
        """
        Initializes trigger
        """
        self._initialized = True
        self._isConditionsComplete = False

    def _setState(self, isConditionsComplete):
        if self._isConditionsComplete != isConditionsComplete:
            self._isConditionsComplete = isConditionsComplete
            self.onStateChanged(self, self._isConditionsComplete)

    def _failed(self):
        self.onFailed(self)