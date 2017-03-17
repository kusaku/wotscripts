# Embedded file name: scripts/common/updatable/UpdatableManager.py
import BigWorld
from struct import pack
from UpdatableObjectBase import *
from Rocket import RocketUpdatable
from Ballistic import BallisticUpdatable
from Bomb import Bomb
from consts import *
from AvatarControllerBase import AvatarControllerBase
from Event import Event, EventOrdered, EventManager
from debug_utils import *
UPDATABLE_TYPE_TO_CLASS_MAP = {UPDATABLE_TYPE.ROCKET: RocketUpdatable,
 UPDATABLE_TYPE.BOMB: Bomb,
 UPDATABLE_TYPE.BALLISTIC: BallisticUpdatable}
if IS_CLIENT:
    g_instance = None

    def Init(owner):
        global g_instance
        if g_instance == None:
            g_instance = UpdatableObjectManager(owner, False)
        return g_instance


    def Destroy():
        global g_instance
        if g_instance != None:
            g_instance.destroy()
            g_instance = None
        return


class UpdatableObjectManager(AvatarControllerBase):

    def __init__(self, owner, isParent = False):
        AvatarControllerBase.__init__(self, owner)
        self.__updatableList = []
        self.__isParent = isParent
        self.__lastCreatedID = 0
        self.__newStates = {}
        self.__eventManager = EventManager()
        em = self.__eventManager
        self.onUpdatableStateChanged = Event(em)

    def __createUpdatableObject(self, typeID):
        return UPDATABLE_TYPE_TO_CLASS_MAP[typeID](self._owner)

    def backup(self):

        def generateData():
            for updatable in self.__updatableList:
                yield updatable.backup()

        data = list(generateData())
        backupContainer = {'Updatables': data,
         'lastCreatedID': self.__lastCreatedID,
         'newStates': self.__newStates}
        return backupContainer

    def restore(self, backupContainer):
        if 'Updatables' in backupContainer:
            self.__updatableList = []
            for updatableData in backupContainer['Updatables']:
                updatable = self.__createUpdatableObject(updatableData[0])
                updatable.restore(updatableData)
                self.__updatableList.append(updatable)

            self.__lastCreatedID = backupContainer['lastCreatedID']
            self.__newStates = backupContainer['newStates']

    def destroyUpdatables(self):
        for updatable in self.__updatableList:
            updatable.destroy()

        self.__updatableList = []

    def destroy(self):
        self.__eventManager.clear()
        self.onUpdatableStateChanged = None
        AvatarControllerBase.destroy(self)
        self.destroyUpdatables()
        return

    def getOwner(self):
        return self._owner

    def update(self, dt = SERVER_TICK_LENGTH):
        time = self._getCurrentTime()
        for updatable in self.__updatableList:
            if not self.__isParent:
                if updatable.getID() in self.__newStates:
                    for stateData in filter(lambda data: data[1] <= time, self.__newStates[updatable.getID()]):
                        updatable.setState(stateData[0])

                    self.__newStates[updatable.getID()] = filter(lambda data: data[1] > time, self.__newStates[updatable.getID()])
                    if len(self.__newStates[updatable.getID()]) == 0:
                        del self.__newStates[updatable.getID()]
            lastState = updatable.getState()
            updatable.update()
            if self.__isParent and lastState != updatable.getState():
                self.__syncState(updatable, updatable.getStateTimeShift())

        self.__updatableList = filter(lambda a: a.getState() != UPDATABLE_STATE.DESTROY, self.__updatableList)

    def update1sec(self, ms):
        for updatable in self.__updatableList:
            lastState = updatable.getState()
            updatable.update1sec()
            if self.__isParent and lastState != updatable.getState():
                self.__syncState(updatable, updatable.getStateTimeShift())

    def _getCurrentTime(self):
        if IS_CLIENT:
            if BigWorld.player().movementFilter():
                return BigWorld.serverTime() - BigWorld.player().filter.latency
            else:
                return BigWorld.serverTime() - DEFAULT_LATENCY
        else:
            return BigWorld.time()

    def __getUnicID(self):
        self.__lastCreatedID += 1
        if self.__isParent:
            return self._owner.id << 12 | self.__lastCreatedID & 4095
        else:
            return self.__lastCreatedID

    def __syncState(self, updatable, timeShift):
        time = self._getCurrentTime() + timeShift
        if updatable.getSyncType() == UPDATABLE_SYNK_TYPE.OWN_CLIENT:
            if self._owner.hasOwnClient():
                self._owner.ownClient.syncUpdatableState(updatable.getID(), updatable.getState(), time)
        elif updatable.getSyncType() == UPDATABLE_SYNK_TYPE.ALL_CLIENT:
            self._owner.allClients.syncUpdatableState(updatable.getID(), updatable.getState(), time)
        elif updatable.getSyncType() == UPDATABLE_SYNK_TYPE.ARENA:
            self._owner.arenaBase.forAllBaseCall('syncUpdatableState', (updatable.getID(), updatable.getState(), time))

    def __syncCreation(self, updatable):
        if updatable.getSyncType() == UPDATABLE_SYNK_TYPE.OWN_CLIENT:
            if self._owner.hasOwnClient():
                self._owner.ownClient.createUpdatable(*updatable.getCreationArgs())
        elif updatable.getSyncType() == UPDATABLE_SYNK_TYPE.ALL_CLIENT:
            self._owner.allClients.createUpdatable(*updatable.getCreationArgs())
        elif updatable.getSyncType() == UPDATABLE_SYNK_TYPE.ARENA:
            self._owner.arenaBase.forAllBaseCall('createUpdatable', updatable.getCreationArgs())

    def createUpdatableLocal(self, typeID, resourceID, *args):
        id = self.__getUnicID()
        launchTime = self._getCurrentTime()
        args = (launchTime, id) + args
        updatable = self.createUpdatableBase(typeID, resourceID, args)
        if self.__isParent:
            self.__syncCreation(updatable)

    def setUpdatableState(self, id, state, time):
        LOG_DEBUG('Change state:', id, state)
        if id not in self.__newStates:
            self.__newStates[id] = []
        self.__newStates[id].append((state, time))

    def createUpdatableBase(self, typeID, resourceID, args):
        updatable = self.__createUpdatableObject(typeID)
        updatable.baseCreate(typeID, resourceID, args)
        self.__updatableList.append(updatable)
        if self.__isParent:
            updatable.setState(UPDATABLE_STATE.CREATE)
        else:
            self.setUpdatableState(updatable.getID(), UPDATABLE_STATE.CREATE, updatable.getLaunchTime())
        return updatable

    def createUpdatable(self, typeID, resourceID, args):
        updatable = self.__createUpdatableObject(typeID)
        updatable.create(typeID, resourceID, args, self.onUpdatableStateChanged)
        self.__updatableList.append(updatable)
        if self.__isParent:
            updatable.setState(UPDATABLE_STATE.CREATE)
        else:
            self.setUpdatableState(updatable.getID(), UPDATABLE_STATE.CREATE, updatable.getLaunchTime())
        return updatable

    def updatablesPresent(self):
        return len(self.__updatableList) > 0

    def getUpdatables(self):
        return self.__updatableList