# Embedded file name: scripts/client/gui/Scaleform/HUD/VehicleSwitcher.py
__author__ = 's_karchavets'
import GameEnvironment
import BigWorld
from EntityHelpers import EntitySupportedClasses, AvatarFlags
from gui.Scaleform.UIHelper import SQUAD_TYPES
from debug_utils import LOG_ERROR, LOG_WARNING, LOG_TRACE

class VEHICLE_SWITCHER_DIRECTIONS:
    INC = 0
    DEC = 1


_AVATAR_FLAGS_FOR_SKIP = AvatarFlags.DEAD | AvatarFlags.LOST

class _VehicleSwitcherBase:
    _sortedDict = dict()
    _sortedDictReverted = dict()

    def __init__(self):
        pass

    def init(self):
        _VehicleSwitcherBase._initSortedDictVehicles()

    @staticmethod
    def _initSortedDictVehicles():
        _VehicleSwitcherBase._sortedDict = dict([ (avatarInfo['airplaneInfo']['decals'][4], id) for id, avatarInfo in GameEnvironment.getClientArena().avatarInfos.iteritems() if BigWorld.player().teamIndex == avatarInfo['teamIndex'] ])
        _VehicleSwitcherBase._sortedDictReverted = dict([ (value, key) for key, value in _VehicleSwitcherBase._sortedDict.iteritems() ])
        LOG_TRACE('_initSortedDictVehicles', _VehicleSwitcherBase._sortedDict)

    def _inc(self, curRate):
        minRate = min(_VehicleSwitcherBase._sortedDict.keys())
        maxRate = max(_VehicleSwitcherBase._sortedDict.keys())
        if curRate == maxRate:
            newID = self._moveInRange(minRate, maxRate + 1)
        else:
            newID = self._moveInRange(curRate + 1, maxRate + 1)
            if newID == -1:
                newID = self._moveInRange(minRate, curRate)
        return newID

    def _dec(self, curRate):
        minRate = min(_VehicleSwitcherBase._sortedDict.keys())
        maxRate = max(_VehicleSwitcherBase._sortedDict.keys())
        if curRate == minRate:
            newID = self._moveInRange(maxRate, minRate - 1, -1)
        else:
            newID = self._moveInRange(curRate - 1, minRate - 1, -1)
            if newID == -1:
                newID = self._moveInRange(maxRate, curRate, -1)
        return newID

    def _moveInRange(self, start, stop, step = 1):
        clientArena = GameEnvironment.getClientArena()
        for key in range(start, stop, step):
            ID = _VehicleSwitcherBase._sortedDict.get(key, None)
            if ID is not None and BigWorld.player().id != ID:
                avatarInfo = clientArena.getAvatarInfo(ID)
                if not avatarInfo['stats']['flags'] & _AVATAR_FLAGS_FOR_SKIP != 0:
                    if self._validate(ID):
                        return ID

        return -1

    def _validate(self, id):
        return True

    def isEnabled(self):
        return True

    def destroy(self):
        pass

    def fire(self, direction):
        id = BigWorld.player().curVehicleID
        if not id:
            id = BigWorld.player().id
        curRate = _VehicleSwitcherBase._sortedDictReverted.get(id, -1)
        if curRate == -1:
            return -1
        elif direction == VEHICLE_SWITCHER_DIRECTIONS.INC:
            return self._inc(curRate)
        elif direction == VEHICLE_SWITCHER_DIRECTIONS.DEC:
            return self._dec(curRate)
        else:
            LOG_ERROR('fire - unknown direction', direction)
            return -1


class _VehicleSwitcherSquad(_VehicleSwitcherBase):

    def __init__(self):
        _VehicleSwitcherBase.__init__(self)
        self.__squad = list()

    def fire(self, direction):
        id = _VehicleSwitcherBase.fire(self, direction)
        self.__squad.append(id)
        return id

    def isEnabled(self):
        return bool([ id for id in _VehicleSwitcherBase._sortedDictReverted.keys() if not GameEnvironment.getClientArena().getAvatarInfo(id)['stats']['flags'] & _AVATAR_FLAGS_FOR_SKIP != 0 and self._validate(id) and id != BigWorld.player().id ])

    def _validate(self, id):
        return id not in self.__squad and SQUAD_TYPES.OWN == SQUAD_TYPES().getSquadType(SQUAD_TYPES().getSquadIDbyAvatarID(id), id)


class _VehicleSwitcher(_VehicleSwitcherBase):
    pass


class VehicleSwitchManager(_VehicleSwitcherBase):

    def __init__(self):
        _VehicleSwitcherBase.__init__(self)
        self.__swithers = list()
        self.__swithers.append(_VehicleSwitcherSquad())
        self.__swithers.append(_VehicleSwitcher())
        self.__inited = False

    def init(self):
        for swither in self.__swithers:
            swither.init()

    def fire(self, direction):
        if not self.__inited:
            self.init()
        self.__inited = True
        newID = -1
        for swither in self.__swithers:
            if swither.isEnabled():
                newID = swither.fire(direction)
                break

        if newID == -1:
            self.init()
            LOG_WARNING('id for switch = -1', direction, [ (id, avatarInfo['stats']['flags']) for id, avatarInfo in GameEnvironment.getClientArena().avatarInfos.iteritems() ])
        return newID

    def destroy(self):
        for swither in self.__swithers:
            swither.destroy()

        self.__swithers = list()