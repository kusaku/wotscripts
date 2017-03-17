# Embedded file name: scripts/client/gui/Scaleform/PartSender.py
"""
Example:

# add object to pool
PartSender().addToPool(poolType, objectsList);

# portion of object that will be removed in each call of 'removeFromPool'
PartSender().setPartSize(poolType, partSize);

PartSender().setPeriodTime(poolType, time_in_sec);

# will be called all time when part of pool was removed
PartSender().setRemoveFromPoolCallback(poolType, partCallback);

# will be called at the end of pool
PartSender().setFinishCallback(poolType, finishCallback);

# start removing from pool with time that was set in setPeriodTime
# if period time equals 'zero' than use removeFromPool all time when needed to remove
# next part of pool with partSize that was set in setPartSize
PartSender().removeFromPool(poolType);
"""
import BigWorld
import threading
from Singleton import singleton
from Event import Event
from functools import partial
from debug_utils import LOG_DEBUG

@singleton

class PartSender(object):
    POOL_TYPE_CAROUSEL_AIRPLANES = 0
    DEFAULT_PART_SIZE = 5

    class _ObjListData:

        def __init__(self):
            self.objList = []
            self.periodTime = 0
            self.removeCallback = Event()
            self.finishCallback = Event()
            self.partSize = 0

    @staticmethod
    def instance():
        return PartSender()

    def __init__(self):
        self.__pool = {}
        self.__poolCallbacks = {}
        self.__lock = threading.RLock()

    def addToPool(self, poolType, objList):
        self.__lock.acquire()
        data = PartSender._ObjListData()
        data.objList = objList
        if poolType in self.__pool:
            self.__pool[poolType].objList += objList
        else:
            self.__pool[poolType] = data
        self.__lock.release()
        LOG_DEBUG('Pool consist of: ', self.__pool)

    def setPartSize(self, poolType, objCount):
        if poolType in self.__pool:
            self.__pool[poolType].partSize = objCount

    def setPeriodTime(self, poolType, time):
        if poolType not in self.__pool:
            return
        self.__pool[poolType].periodTime = time

    def setRemoveFromPoolCallback(self, poolType, callback):
        if poolType in self.__pool:
            self.__pool[poolType].removeCallback = callback

    def setFinishCallback(self, poolType, callback):
        if poolType in self.__pool:
            self.__pool[poolType].finishCallback = callback

    def clearPool(self, poolType):
        if poolType in self.__pool:
            del self.__pool[poolType]

    def clearAllPools(self):
        self.__pool.clear()

    def clearCallbacks(self):
        for callback in self.__poolCallbacks:
            BigWorld.cancelCallback(callback)

        self.__poolCallbacks = {}

    def removeFromPool(self, poolType):
        LOG_DEBUG('removeFromPool', poolType)
        if poolType not in self.__pool:
            return
        data = self.__pool[poolType]
        LOG_DEBUG('data.partSize', data.partSize)
        LOG_DEBUG('pool len', len(self.__pool[poolType].objList))
        if data.partSize > 0:
            self.__lock.acquire()
            partObjList = self.__pool[poolType].objList[:data.partSize]
            del self.__pool[poolType].objList[:data.partSize]
            self.__pool[poolType].removeCallback(partObjList)
            LOG_DEBUG('pool len after remove', len(self.__pool[poolType].objList))
            self.__lock.release()
        if len(self.__pool[poolType].objList) > 0:
            if data.periodTime > 0:
                self.__poolCallbacks[poolType] = BigWorld.callback(data.periodTime, partial(self.removeFromPool, poolType))
        else:
            self.__pool[poolType].finishCallback()
            self.clearPool(poolType)