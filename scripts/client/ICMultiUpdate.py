# Embedded file name: scripts/client/ICMultiUpdate.py
from abc import ABCMeta, abstractmethod
import BigWorld

class ICMultiUpdate(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        self.__items = args
        self.__callBack = [None] * len(args)
        self.__suspend = True
        self._StartUpdates()
        return

    def _StartUpdates(self):
        if self.__suspend:
            self.__suspend = False
            for index, item in enumerate(self.__items):
                self.__updateCallBack(index, item)

    def _SuspendUpdates(self):
        if not self.__suspend:
            self.__suspend = True
            for index in range(0, len(self.__items)):
                BigWorld.cancelCallback(self.__callBack[index])

    def __updateCallBack(self, index, item):
        item[1]()
        self.__callBack[index] = BigWorld.callback(item[0], lambda : self.__updateCallBack(index, item))

    @abstractmethod
    def restart(self):
        self._SuspendUpdates()
        self._StartUpdates()

    @abstractmethod
    def dispose(self):
        if not self.__suspend:
            for index in range(0, len(self.__items)):
                BigWorld.cancelCallback(self.__callBack[index])

        self.__suspend = None
        self.__items = None
        self.__callBack = None
        return