# Embedded file name: scripts/client/gui/AlwaysVisibleObjects.py
import GameEnvironment
import Math
from MapEntry import MapEntry
import BigWorld
from debug_utils import LOG_DEBUG
from EntityHelpers import unpackPositionFrom2DTuple, EntitySupportedClasses, EntityStates, unpackAngleFromByte

class AlwaysVisibleObjects:

    def __init__(self):
        self.__list = {}

    def addAllTimeVisibleObject(self, entityID, classID, teamIndex, position, alive, modelID):
        """
        add object which must be visible on the map whole game time
        
        @param entityID: object ID
        @type entityID:int
        @param classID: EntitySupportedClasses const
        @type classID: int
        @param teamIndex: (0 or 1)
        @type teamIndex: int
        @param position: position for static objects
        @type position: Vector3
        @param alive: is object alive at this time (could be changed for restorable objects)
        @type alive: boolean
        @param modelID: object ID to get it settings
        @type modelID: int
        """
        self.__list[entityID] = MapEntry(entityID, classID, teamIndex, position, alive, modelID)
        self.__updateObjectVisibility(self.__list[entityID])

    def updateTemporaryVisibleObjectData(self, objectUpdatableData, objectClassID, objectTeamIndex, modelID):
        """
        add new object info or update it.
        Used for objects which could not be visible because of Bigworld issue
        
        @param objectUpdatableData:
        @type objectUpdatableData: {"id", "position", "isVisible", "angle"}
        @param objectClassID: EntitySupportedClasses const
        @type objectClassID: int
        @param objectTeamIndex: 0 or 1
        @type objectTeamIndex: int
        @param modelID: object ID to get it settings
        @type modelID: int
        """
        id = objectUpdatableData['id']
        needRefresh = False
        if id not in self.__list:
            self.__list[id] = MapEntry(id, objectClassID, objectTeamIndex, Math.Vector3(), objectUpdatableData['isVisible'], modelID)
            needRefresh = True
            if BigWorld.entities.has_key(id):
                BigWorld.entities[id].onMapEntryCreated(self.__list[id])
        elif self.__list[id].isAlive != objectUpdatableData['isVisible']:
            needRefresh = True
            self.__list[id].isAlive = objectUpdatableData['isVisible']
        mapEntry = self.__list[id]
        if mapEntry.isAlive:
            arenaData = GameEnvironment.getClientArena().arenaData
            x, z = unpackPositionFrom2DTuple(objectUpdatableData['position'], arenaData['bounds'])
            mapEntry.setPositionAndYaw(Math.Vector3(x, 0, z), unpackAngleFromByte(objectUpdatableData['yaw']))
        if needRefresh and (not BigWorld.entities.has_key(id) or EntityStates.inState(BigWorld.entities[id], EntityStates.DEAD)):
            self.__updateObjectVisibility(mapEntry)

    def getMapEntry(self, objID):
        """return map entry for objID if present"""
        mapEntry = self.__list.get(objID, None)
        return mapEntry

    def getObjectName(self, id):
        if id in self.__list:
            return EntitySupportedClasses.getClassNameByID(self.__list[id].classID)
        else:
            return None

    def __updateObjectVisibility(self, obj):
        GameEnvironment.getHUD().updateObjectVisibility(obj)