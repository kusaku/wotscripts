# Embedded file name: scripts/common/MultiUpdate.py
__author__ = 'm_pavlenko'
import BigWorld
from consts import IS_CLIENT
from functools import partial

class MultiUpdate(object):

    def __init__(self, *args):
        self.__items = args
        self.__callBack = [None] * len(args)
        self.__suspend = True
        self.__startUpdates()
        return

    def __addUpdate(self, dt, func):
        if IS_CLIENT:
            return BigWorld.callback(dt, func)
        else:
            return BigWorld.addTimer(func, dt)

    def __removeUpdate(self, id):
        if IS_CLIENT:
            BigWorld.cancelCallback(id)
        else:
            BigWorld.delTimer(id)

    def __startUpdates(self):
        if self.__suspend:
            self.__suspend = False
            for index, item in enumerate(self.__items):
                self.__callBack[index] = self.__addUpdate(item[0], partial(self.__updateCallBack, index, item))

    def __suspendUpdates(self):
        if not self.__suspend:
            self.__suspend = True
            for index in xrange(len(self.__items)):
                self.__removeUpdate(self.__callBack[index])

    def __updateCallBack(self, index, item, iD = 0, userArg = 0):
        dt, uFunc = item
        uFunc()
        if iD:
            self.__removeUpdate(iD)
        self.__callBack[index] = self.__addUpdate(dt, partial(self.__updateCallBack, index, item))

    def dispose(self):
        if not self.__suspend:
            for index in xrange(len(self.__items)):
                self.__removeUpdate(self.__callBack[index])

        self.__suspend = None
        self.__items = None
        self.__callBack = None
        return