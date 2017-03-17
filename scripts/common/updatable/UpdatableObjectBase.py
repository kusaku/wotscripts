# Embedded file name: scripts/common/updatable/UpdatableObjectBase.py
import BigWorld
from struct import pack, unpack
from consts import *

class UPDATABLE_STATE:
    NONE = 0
    CREATE = 1
    DESTROY = 2
    ON_THE_GROUND = 3
    EXPLODED = 4


class UPDATABLE_SYNK_TYPE:
    NONE = 0
    OWN_CLIENT = 1
    ALL_CLIENT = 2
    ARENA = 3


class UPDATABLE_STATE_CB:
    NONE = 0
    MODEL_LOADED = 1
    EXPLODED = 2


class Modifiers(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class UpdatableObjectBase(object):
    BACKUP_SIGNATURE_STRING = 'dqi'
    SEND_SIGNATURE_STRING = 'dq'

    def __init__(self, owner):
        self._owner = owner
        self._launchTime = 0.0
        self._id = 0
        self.__state = UPDATABLE_STATE.NONE
        self._updatableTypeId = 0
        self._resourceID = 0
        self.__stateTimeShift = 0.0
        self._stateCB = None
        return

    def getStateTimeShift(self):
        return self.__stateTimeShift

    def getUpdatableTypeID(self):
        return self._updatableTypeId

    def getCreationArgs(self):
        pass

    def backup(self):
        packList = [self._launchTime, self._id, self.__state]
        return [self._updatableTypeId, self._resourceID, pack(UpdatableObjectBase.BACKUP_SIGNATURE_STRING, *packList)]

    def restore(self, data):
        self._stateCB = None
        self._updatableTypeId = data[0]
        self._resourceID = data[1]
        self._launchTime, self._id, self.__state = unpack(UpdatableObjectBase.BACKUP_SIGNATURE_STRING, data[2])
        return

    def getID(self):
        return self._id

    def creatorOwnerID(self):
        return self._id >> 12

    def getLaunchTime(self):
        return self._launchTime

    def getSyncType(self):
        return UPDATABLE_SYNK_TYPE.ALL_CLIENT

    def baseCreate(self, typeID, resourceID, args):
        self._updatableTypeId = typeID
        self._resourceID = resourceID
        self._onBaseCreate(args)

    def create(self, typeID, resourceID, args, stateCB = None):
        self._updatableTypeId = typeID
        self._resourceID = resourceID
        self._stateCB = stateCB
        self._onCreate(args)

    def _onCreate(self, *arg):
        pass

    def _onBaseCreate(self, *arg):
        pass

    def destroy(self):
        self._stateCB = None
        self._owner = None
        return

    def setState(self, state, timeShift = 0.0):
        self.__stateTimeShift = timeShift
        self.__state = state

    def getState(self):
        return self.__state

    def _getCurrentTime(self):
        if IS_CLIENT:
            if BigWorld.player().movementFilter():
                return BigWorld.serverTime() - BigWorld.player().filter.latency - self._launchTime
            else:
                return BigWorld.serverTime() - DEFAULT_LATENCY - self._launchTime
        else:
            return BigWorld.time() - self._launchTime

    def _positionUpdate(self):
        pass

    def update(self):
        self._positionUpdate()

    def update1sec(self):
        pass

    def getPackArgs(self):
        return pack(UpdatableObjectBase.SEND_SIGNATURE_STRING, self._launchTime, self._id)

    def setUnpackArgs(self, args):
        if isinstance(args, str):
            self._launchTime, self._id = unpack(UpdatableObjectBase.SEND_SIGNATURE_STRING, args)
        else:
            self._launchTime, self._id = args

    def getOwner(self):
        return self._owner