# Embedded file name: scripts/client/gui/event_boards/listener.py
from gui.shared.utils.listeners_collection import ListenersCollection

class IEventBoardsListener(ListenersCollection):

    def __init__(self):
        super(IEventBoardsListener, self).__init__()
        self._setListenerClass(IEventBoardsListener)

    def onUpdateHangarFlag(self):
        """
        Establishes a listener when need update hangar flag
        """
        pass