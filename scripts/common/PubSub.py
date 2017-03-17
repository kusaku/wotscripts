# Embedded file name: scripts/common/PubSub.py
from collections import defaultdict

class PubSub:

    def __init__(self):
        self._subscribedEvents = defaultdict(list)

    def _clean(self):
        self._subscribedEvents.clear()

    def publish(self, event, *args):
        raise self.__isValidhArgs(event, *args) or AssertionError
        for callback in self._subscribedEvents[event[0]]:
            callback(*args)

    def subscribe(self, event, callback):
        if not self.__isValidEvent(event):
            raise AssertionError
            subscribers = self._subscribedEvents[event[0]]
            callback not in subscribers and subscribers.append(callback)

    def __isValidEvent(self, event):
        return True

    def __isValidhArgs(self, event, *args):
        raise self.__isValidEvent(event) or AssertionError
        return True