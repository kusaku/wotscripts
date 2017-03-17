# Embedded file name: scripts/client/gui/Scaleform/HUD/Counter.py
__author__ = 's_karchavets'
from debug_utils import LOG_DEBUG

class CounterBase(object):

    def __init__(self, resultCount, fireCallback = None, finalCallback = None):
        self._count = 0
        self._resultCount = resultCount
        self._finalCallback = finalCallback
        self._fireCallback = fireCallback

    def reset(self):
        self._count = 0

    def fire(self):
        if self._fireCallback is not None:
            self._fireCallback(self._resultCount - self._count)
        return

    def _finish(self):
        LOG_DEBUG('fire - count is finished.', self._count, self._resultCount)
        if self._finalCallback is not None:
            self._finalCallback(self._resultCount - self._count)
        return

    def check(self):
        pass

    def destroy(self):
        self._finalCallback = None
        self._fireCallback = None
        return


class IncCounter(CounterBase):

    def fire(self):
        if self.check():
            self._count += 1
            CounterBase.fire(self)
        else:
            CounterBase._finish(self)

    def check(self):
        return self._count < self._resultCount


class DecCounter(CounterBase):

    def fire(self):
        if self.check():
            self._count -= 1
            CounterBase.fire(self)
        else:
            CounterBase._finish(self)

    def check(self):
        return self._count > self._resultCount