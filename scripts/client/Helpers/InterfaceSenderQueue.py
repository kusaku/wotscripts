# Embedded file name: scripts/client/Helpers/InterfaceSenderQueue.py
import BigWorld
from clientConsts import INTERFACE_QUERY_PERIOD
from collections import deque

class InterfaceSenderQueue(object):
    _queue = None
    _timerID = None
    _sender = None

    def __init__(self, sender):
        self._queue = deque()
        self._sender = sender

    def queueQuery(self, request, callback):
        if self._timerID is None:
            self._sender.getIfaceData(request, callback)
            self._setTimer()
            return
        else:
            self._queue.append((request, callback))
            return

    def _setTimer(self):
        self._timerID = BigWorld.callback(INTERFACE_QUERY_PERIOD, self._processQueue)

    def _processQueue(self):
        BigWorld.cancelCallback(self._timerID)
        if not self._queue:
            self._timerID = None
            return
        else:
            self._sender.getIfaceData(*self._queue.popleft())
            self._setTimer()
            return

    def destroy(self):
        if self._timerID is not None:
            BigWorld.cancelCallback(self._timerID)
            self._timerID = None
        self._sender = None
        self._queue = None
        return