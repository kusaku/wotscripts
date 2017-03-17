# Embedded file name: scripts/client/gui/MapBase.py
import Math
import GUI
import BigWorld
import db.DBLogic
from debug_utils import LOG_DEBUG, LOG_ERROR
from gui.HUDconsts import *
from gui.Scaleform.UIHelper import SQUAD_TYPES
from consts import DB_PATH, PLANE_TYPE, TEAM_OBJECT_CLASS_NAMES
import ResMgr
from HudElements.IngameChat import ChatMessagesStringID
import GameEnvironment
from EntityHelpers import EntitySupportedClasses
from clientConsts import TEAM_OBJECTS_PARTS_TYPES

class MarkerType():
    DEFAULT = 0
    BASE_UNDER_ATTACK = 1


class NAVIGATION_WINDOWS_STATES():
    NORMAL = 0
    BLIND = 1


class VisibilityRangeType():
    ONE_TEXTURE_ONE_MESH = 0
    ONE_TEXTURE_TWO_MESHES = 1


class MapBase():
    GROUPS_MARKERS_WITH_ROTATION = []
    GROUPS_MARKERS_COUNT = 6
    GROUPS_MARKERS_TEXTURE_ID = 'HUD_MAP_TACTICS_MARKER_GROUP%s'
    VR_DIRECTION_LINE_COLOR = Math.Vector4(187, 187, 187, 150)
    VR_ATLAS_TEXTURE = 'gui/maps/atlas.dds'
    VR_DESC_ATLAS = 'gui/maps/atlas.tai'
    VR_SECTOR_TEXTURE = 'gui/maps/hudRadarSectorNew.dds'
    VR_OVERLAY_TEXTURE = 'gui/maps/hudRadarCircleBg.dds'
    VR_MASK_TEXTURE = 'gui/maps/hudMapRadarSector.dds'
    __RESOURCES_PATH = DB_PATH + 'navigation_windows.xml'
    BASE_OBJECT_DEPTH = 1.0
    TEAM_OBJECT_DEPTH = 0.95
    MIN_ENTRY_DEPTH = 0.8
    MAX_ENTRY_DEPTH = 0.7
    PLAYER_DEPTH = 0.6
    TARGET_DEPTH = 0.55
    ENTITY_COMMAND_DEPTH = 0.5
    DOMITATION_LAYER = 1
    AREAS_LAYER = 10
    FRIEND_COLOR = (0, 255, 0, 128)
    ENEMY_COLOR = (255, 0, 0, 128)
    PLAYER_COLOR = (255, 255, 255, 255)
    PLAYER_COLOR_SQUAD = (255, 255, 255, 255)
    DOMINATION_ARROW_CLOLOR = 4294967040L
    ENTITY_FRIEND = 0
    ENTITY_ENEMY = 1
    ENTITY_LOCKED = 2
    ENTITY_PLAYER = 3
    ENTITY_PLAYER_SQUAD = 4
    ENTITY_TEAM_KILLER = 5
    ALT_STATES = {PLANE_TYPE.ASSAULT: {NAVIGATION_WINDOWS_STATES.NORMAL: HUD_NAV_WINDOWS_STATE_ALT_ASSAULT,
                          NAVIGATION_WINDOWS_STATES.BLIND: HUD_NAV_WINDOWS_STATE_ALT_ASSAULT_BLIND},
     PLANE_TYPE.FIGHTER: {NAVIGATION_WINDOWS_STATES.NORMAL: HUD_NAV_WINDOWS_STATE_ALT_FIGHTER,
                          NAVIGATION_WINDOWS_STATES.BLIND: HUD_NAV_WINDOWS_STATE_ALT_FIGHTER_BLIND},
     PLANE_TYPE.HFIGHTER: {NAVIGATION_WINDOWS_STATES.NORMAL: HUD_NAV_WINDOWS_STATE_ALT_HFIGHTER,
                           NAVIGATION_WINDOWS_STATES.BLIND: HUD_NAV_WINDOWS_STATE_ALT_HFIGHTER_BLIND},
     PLANE_TYPE.NAVY: {NAVIGATION_WINDOWS_STATES.NORMAL: HUD_NAV_WINDOWS_STATE_ALT_NAVY,
                       NAVIGATION_WINDOWS_STATES.BLIND: HUD_NAV_WINDOWS_STATE_ALT_NAVY_BLIND}}
    ALT_STATES_TEAM_OBJECTS = {TEAM_OBJECTS_PARTS_TYPES.SIMPLE: 2,
     TEAM_OBJECTS_PARTS_TYPES.SIMPLE_ARMORED: 3,
     TEAM_OBJECTS_PARTS_TYPES.SIMPLE_FIRING: 4,
     TEAM_OBJECTS_PARTS_TYPES.SIMPLE_FIRING_ARMORED: 5,
     TEAM_OBJECTS_PARTS_TYPES.ARMORED: 6,
     TEAM_OBJECTS_PARTS_TYPES.FIRING_ARMORED: 7}

    def __init__(self):
        self._state = 0
        self.__entityComponentDataState = None
        self._isAltState = False
        self._entityObject = dict()
        self.entities = {}
        self._lockTargetData = {'entityID': None,
         'ID': None}
        self._visible = False
        self.objectsAreaTexture = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_DOMINATION_TEXTURE_OWN'))
        self.map = None
        self.markerEntities = {MarkerType.DEFAULT: db.DBLogic.g_instance.getGUITexture('TX_MAP_TARGET'),
         MarkerType.BASE_UNDER_ATTACK: db.DBLogic.g_instance.getGUITexture('TX_MAP_TARGET_ATTACK')}
        return

    def setState(self, val):
        if val != self._state:
            self._state = val
            self.__entityComponentDataState = None
            self._updateState()
        return

    def destroy(self):
        self.setVisible(False)

    def isVisible(self):
        return self._visible

    def setVisible(self, isVisible):
        if self._visible != isVisible:
            self._visible = isVisible
            self._updateGUIVisibility(isVisible)

    def _updateGUIVisibility(self, isVisible):
        pass

    def _prepareVisibilityRangeData(self):
        pass

    def _setVisibleLocked(self, isVisible):
        if self._lockTargetData['ID'] is not None:
            component = self.map.getEntityComponent(self._lockTargetData['ID'])
            if component is not None:
                component.visible = isVisible
        return

    def setLocked(self, entity, isLocked):
        if entity.id in self.entities:
            self.clearLockedData()
            if isLocked:
                entityComponentData = self._getResContainer().ENTITY_COMPONENTS[self._state][entity.getMapTexture()]
                if self.ENTITY_LOCKED >= len(entityComponentData):
                    LOG_DEBUG('setLocked - without lock texture', entity.id, self._state)
                    return
                component = self.getEntityGUI('', MapBase.ENEMY_COLOR)
                component.position = (0, 0, MapBase.TARGET_DEPTH)
                entityComponentData = entityComponentData[self.ENTITY_LOCKED]
                component.textureName = db.DBLogic.g_instance.getGUITexture(entityComponentData['texture'])
                if 'color' in entityComponentData:
                    component.colour = entityComponentData['color']
                component.size = entityComponentData['size']
                self._lockTargetData['ID'] = self.map.add(entity.mapMatrix, component, '', True, True)
                self._lockTargetData['entityID'] = entity.id

    def clearLockedData(self):
        if self._lockTargetData['ID'] is not None:
            self.map.remove(self._lockTargetData['ID'])
            self._lockTargetData['entityID'] = None
            self._lockTargetData['ID'] = None
        return

    def remove(self, entity):
        self._removeEntityObject(entity.id)
        if entity.id in self.entities:
            self.map.remove(self.entities[entity.id])
            if self._lockTargetData['entityID'] == entity.id:
                self.clearLockedData()
            del self.entities[entity.id]

    def getEntityGUI(self, path, color):
        c = GUI.Simple(path)
        c.materialFX = 'BLEND'
        c.colour = color
        c.widthMode = 'PIXEL'
        c.heightMode = 'PIXEL'
        c.size = (32, 32)
        c.filterType = 'LINEAR'
        return c

    def setMarker(self, posX, posZ, markerType = MarkerType.DEFAULT, blinkNum = 3):
        entityMarker = self.getEntityGUI(self.markerEntities[markerType], MapBase.PLAYER_COLOR)
        entityMarker.colour = MapBase.PLAYER_COLOR if markerType == MarkerType.DEFAULT else MapBase.ENEMY_COLOR
        if markerType == MarkerType.BASE_UNDER_ATTACK:
            entityMarker.size = (52, 52)
        mtxPos = Math.Matrix()
        mtxPos.setTranslate((posX, 1.0, posZ))
        self.map.addMarker(mtxPos, entityMarker, MAP_BLINK_PERIOD, blinkNum, markerType, False, False)

    def setEntityCommand(self, senderID, pMatrix, commandID):
        """
        set entity command on the map
        @param senderID: int
        @param pMatrix: MatrixProviderPtr
        @param commandID: ChatMessagesStringID
        """
        container = self._getResContainer()
        entityCommand = self.getEntityGUI('', MapBase.PLAYER_COLOR)
        entityCommand.textureName = db.DBLogic.g_instance.getGUITexture(container.ENTITY_COMPONENTS[self._state][HUD_MINIMAP_ENTITY_TYPE_COMMAND][commandID]['texture'])
        entityCommand.size = container.ENTITY_COMPONENTS[self._state][HUD_MINIMAP_ENTITY_TYPE_COMMAND][commandID]['size']
        entityCommand.position = (0, 0, MapBase.ENTITY_COMMAND_DEPTH)
        self.map.addMarker(pMatrix, entityCommand, MAP_ENTITY_COMMAND_BLINK_PERIOD, MAP_ENTITY_COMMAND_BLINK_NUM, MarkerType.DEFAULT, True, True)

    def addAnyObjectWithBlink(self, pMatrix, entityType, entitySubType, blinkPeriod, blinkNum, lockRotation = True, lockDepth = True):
        container = self._getResContainer()
        pComponent = self.getEntityGUI('', MapBase.PLAYER_COLOR)
        pComponent.textureName = db.DBLogic.g_instance.getGUITexture(container.ENTITY_COMPONENTS[self._state][entityType][entitySubType]['texture'])
        pComponent.size = container.ENTITY_COMPONENTS[self._state][entityType][entitySubType]['size']
        pComponent.position = (0, 0, MapBase.ENTITY_COMMAND_DEPTH)
        self.map.addMarker(pMatrix, pComponent, blinkPeriod, blinkNum, MarkerType.DEFAULT, lockRotation, lockDepth)

    def drawObjectsAreas(self, areas):
        fID = self.__class__.__name__ + '.drawObjectsAreas()'
        for i, areaData in enumerate(areas):
            size = (areaData['r'] * 2.0, areaData['r'] * 2.0)
            self.map.addTextureLayer(MapBase.AREAS_LAYER + i, self.objectsAreaTexture, size, areaData['pos'])

    def setupComponent(self, entity, component, locked):
        enityState = self.ENTITY_LOCKED
        if not locked:
            enityState = self.__getEnityStateSquad(entity)
        entityType = entity.getMapTexture()
        if self.__entityComponentDataState is None:
            self.__entityComponentDataState = self._getResContainer().ENTITY_COMPONENTS[self._state]
        entityComponentDataStateType = self.__entityComponentDataState[entityType]
        upTexture = ''
        lock = False
        if entity is BigWorld.player():
            enityState = self.ENTITY_PLAYER
            entityComponentData = entityComponentDataStateType[enityState]
        else:
            entityComponentData = entityComponentDataStateType[enityState]
            if 'up_texture' in entityComponentData:
                upTexture = db.DBLogic.g_instance.getGUITexture(entityComponentData['up_texture'])
            if 'lock' in entityComponentData:
                lock = entityComponentData['lock']
        component.textureName = db.DBLogic.g_instance.getGUITexture(entityComponentData['texture'])
        if 'color' in entityComponentData:
            component.colour = entityComponentData['color']
        if 'size' in entityComponentData:
            component.size = entityComponentData['size']
        return (entityType,
         enityState,
         upTexture,
         lock)

    def createComponents(self, entity):
        entityComponentData = self._getResContainer().ENTITY_COMPONENTS[self._state][entity.getMapTexture()][self.ENTITY_FRIEND]
        return (self.getEntityGUI('', (255, 255, 255, 255)), self.getEntityGUI('', (255, 255, 255, 255)) if 'up_texture' in entityComponentData else None)

    def __getEnityStateSquad(self, entity):
        """
        get enity state for squad
        @param entity:
        @return: (int) enityState
        """
        enityState = self.ENTITY_ENEMY
        player = BigWorld.player()
        if entity.teamIndex == player.teamIndex:
            enityState = self.ENTITY_FRIEND
            squadType = SQUAD_TYPES.getSquadType(SQUAD_TYPES.getSquadIDbyAvatarID(entity.id), entity.id)
            if squadType == SQUAD_TYPES.OWN:
                enityState = self.ENTITY_PLAYER_SQUAD
        return enityState

    @staticmethod
    def _getPreloadedResources(container):
        """
        @param container: MapBase
        @return: list
        """
        resourceList = []
        for stateData in container.ENTITY_COMPONENTS.values():
            for entityData in stateData.values():
                for entitySubtypeData in entityData.values():
                    if entitySubtypeData:
                        resourceList.append(db.DBLogic.g_instance.getGUITexture(entitySubtypeData['texture']))
                        if 'up_texture' in entitySubtypeData:
                            resourceList.append(db.DBLogic.g_instance.getGUITexture(entitySubtypeData['up_texture']))

        return resourceList

    def _getResContainer(self):
        pass

    def _updateState(self):
        """
        update only texture now
        """
        container = self._getResContainer()
        for id, entityObject in self._entityObject.items():
            if id in self.entities:
                if self._state in container.ENTITY_COMPONENTS:
                    if entityObject[1] in container.ENTITY_COMPONENTS[self._state]:
                        if entityObject[2] in container.ENTITY_COMPONENTS[self._state][entityObject[1]]:
                            entityComponent = self.map.getEntityComponent(self.entities[id])
                            if entityComponent:
                                if 'texture' in container.ENTITY_COMPONENTS[self._state][entityObject[1]][entityObject[2]]:
                                    texture = db.DBLogic.g_instance.getGUITexture(container.ENTITY_COMPONENTS[self._state][entityObject[1]][entityObject[2]]['texture'])
                                    entityComponent.textureName = texture
                                    if 'up_texture' in container.ENTITY_COMPONENTS[self._state][entityObject[1]][entityObject[2]]:
                                        up_texture = db.DBLogic.g_instance.getGUITexture(container.ENTITY_COMPONENTS[self._state][entityObject[1]][entityObject[2]]['up_texture'])
                                        self.map.setTexture(self.entities[id], texture, up_texture)
                                if entityObject[1] == HUD_MINIMAP_ENTITY_TYPE_AVATAR:
                                    self.map.setLockRotation(self.entities[id], False)
                        else:
                            LOG_ERROR('_updateState - entitySubtype(%s) not in ENTITY_COMPONENTS' % entityObject[2])
                    else:
                        LOG_ERROR('_updateState - entityType(%s) not in ENTITY_COMPONENTS' % entityObject[1])
                else:
                    LOG_ERROR('_updateState - self._state(%s) not in ENTITY_COMPONENTS' % self._state)
            else:
                LOG_ERROR('_updateState - id(%s) not in self.entities' % id)

    def setAltState(self, isFired):
        self._isAltState = isFired
        if isFired:
            self._updateAltState()
        else:
            self._updateState()

    def add(self, entity, c, entityType, enityState):
        clientArena = GameEnvironment.getClientArena()
        if entityType == HUD_MINIMAP_ENTITY_TYPE_AVATAR:
            targetType = clientArena.getAvatarInfo(entity.id)['settings'].airplane.planeType
        else:
            targetType = clientArena.getTeamObjectType(entity.id)
        self._addEntityObject(entity.id, c, entityType, enityState, targetType)
        if entityType == HUD_MINIMAP_ENTITY_TYPE_AVATAR and self._isAltState:
            self.setAltState(self._isAltState)

    def _updateAltState(self):
        container = self._getResContainer()
        for id, entityObject in self._entityObject.items():
            if id != BigWorld.player().id:
                entity = entityObject[1]
                if entity == HUD_MINIMAP_ENTITY_TYPE_AVATAR:
                    if id in self.entities:
                        objType = entityObject[3]
                        if objType in MapBase.ALT_STATES:
                            state = MapBase.ALT_STATES[objType][self._state]
                            if state in container.ENTITY_COMPONENTS:
                                entityComponent = self.map.getEntityComponent(self.entities[id])
                                if entityComponent:
                                    self.map.setLockRotation(self.entities[id], True)
                                    texture = db.DBLogic.g_instance.getGUITexture(container.ENTITY_COMPONENTS[state][entity][entityObject[2]]['texture'])
                                    entityComponent.textureName = texture
                                    if 'up_texture' in container.ENTITY_COMPONENTS[state][entityObject[1]][entityObject[2]]:
                                        up_texture = db.DBLogic.g_instance.getGUITexture(container.ENTITY_COMPONENTS[state][entityObject[1]][entityObject[2]]['up_texture'])
                                        self.map.setTexture(self.entities[id], texture, up_texture)
                            else:
                                LOG_ERROR('_updateAltState - state(%s) not in ENTITY_COMPONENTS' % state)
                        else:
                            LOG_ERROR('_updateAltState - objType(%s) not in ALT_STATES' % objType)
                    else:
                        LOG_ERROR('_updateAltState - id(%s) not in self.entities' % id)

    def _addEntityObject(self, id, guiComponent, entity, entitySubtype, objType):
        self._entityObject[id] = (guiComponent,
         entity,
         entitySubtype,
         objType)

    def _removeEntityObject(self, id):
        if id in self._entityObject:
            del self._entityObject[id]

    def _isAvatar(self, entity):
        return not (entity.__class__.__name__ in TEAM_OBJECT_CLASS_NAMES or entity.__class__.__name__ == 'MapEntry' and entity.classID not in [EntitySupportedClasses.Avatar, EntitySupportedClasses.AvatarBot])

    def setSpectatorMode(self, isSpectatorMode):
        pass

    def setBounds(self, bounds):
        pass

    def setVisibility(self, entity, isVisible):
        guiId = self.entities.get(entity.id, None)
        if guiId is not None:
            self.map.setVisibility(guiId, isVisible)
        return

    def setMatrix(self, entity, matrix):
        guiId = self.entities.get(entity.id, None)
        if guiId is not None:
            self.map.setMatrix(guiId, matrix)
        return

    def setBeamMatrix(self, matrix):
        pass

    def setEntityText(self, entity, text):
        pass

    def addGroup(self, groupName, groupEntities):
        pass

    def initGroup(self, groupName, iconIndex):
        pass

    def setVisibilityGroup(self, groupName, isVisible):
        pass


class NavigationWindowsManager(MapBase):

    def __init__(self):
        self.__navigationWindows = list()

    def addNavigationWindow(self, navigationWindow):
        self.__navigationWindows.append(navigationWindow)

    def add(self, entity):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.add(entity)

    def remove(self, entity):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.remove(entity)

    def setLocked(self, entity, isLocked):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setLocked(entity, isLocked)

    def setMarker(self, posX, posZ, markerType, blinkNum):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setMarker(posX, posZ, markerType, blinkNum)

    def setState(self, val):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setState(val)

    def setAltState(self, isFired):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setAltState(isFired)

    def destroy(self):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.destroy()

        self.__navigationWindows = list()

    def setSpectatorMode(self, isSpectatorMode):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setSpectatorMode(isSpectatorMode)

    def setBounds(self, bounds):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setBounds(bounds)

    def setVisibility(self, entity, isVisible):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setVisibility(entity, isVisible)

    def setMatrix(self, entity, matrix):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setMatrix(entity, matrix)

    def setEntityText(self, entity, text):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setEntityText(entity, text)

    def setEntityCommand(self, senderID, pMatrix, commandID):
        for navigationWindow in self.__navigationWindows:
            if navigationWindow.isVisible():
                navigationWindow.setEntityCommand(senderID, pMatrix, commandID)

    def setBeamMatrix(self, matrix):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.map.ownerpoint = matrix

    def initGroup(self, groupName, iconIndex):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.initGroup(groupName, iconIndex)

    def addGroup(self, groupName, groupEntities):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.addGroup(groupName, groupEntities)

    def setVisibilityGroup(self, groupName, isVisible):
        for navigationWindow in self.__navigationWindows:
            navigationWindow.setVisibilityGroup(groupName, isVisible)