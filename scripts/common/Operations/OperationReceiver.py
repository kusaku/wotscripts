# Embedded file name: scripts/common/Operations/OperationReceiver.py
from Event import Event
from Operations.OperationReceiverBase import OperationReceiverBase

class OperationReceiver(OperationReceiverBase):
    """
    Operation receiver
    """

    def __init__(self, sender, loadsTransferType, dumpsTransferType, streamer = None):
        """
        Constructor
        @param sender: operation sender
        @type sender: MAILBOX
        """
        OperationReceiverBase.__init__(self, sender, loadsTransferType, dumpsTransferType, streamer)
        self.onReceiveOperation = Event()

    def _onReceiveOperation(self, operation):
        self.onReceiveOperation(operation)

    def destroy(self):
        """
        Destructor
        """
        OperationReceiverBase.destroy(self)
        self.onReceiveOperation.clear()
        self.onReceiveOperation = None
        return