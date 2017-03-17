# Embedded file name: scripts/client/gui/Minimap.py
import BigWorld
from Event import Event, EventManager
import GUI
import Helpers.PyGUI as PyGUI
import ResMgr
import Math
from MathExt import clamp
from functools import partial
import Cursor
from MapBase import *
import weakref
import Settings
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_WARNING, LOG_CURRENT_EXCEPTION
from HUDconsts import HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE, HUD_MINIMAP_ENTITY_TYPE_COMMAND
from HudElements.IngameChat import ChatMessagesStringID
from EntityHelpers import isAvatar
from wofdecorators import noexcept
from clientConsts import GUI_COMPONENTS_DEPH
from consts import NAVIGATION_WINDOWS_TYPES
import GameEnvironment
from consts import WAITING_QUEUE_MAX_SIZE, GAME_OBJECTS_PER_ARENA_LIMIT, SUPERIORITY2_BASE_HEALTH, MIN_SEND_MARKER_MESSAGE_PERIOD

class MinimapEventHandler:

    def __init__(self, parent):
        self.lastClickTime = 0
        self.__parent = parent

    def handleMouseClickEvent(self, comp):
        if BigWorld.time() - self.lastClickTime > MIN_SEND_MARKER_MESSAGE_PERIOD:
            parentMap = self.__parent()
            if parentMap:
                self.lastClickTime = BigWorld.time()
                cursorPos = GUI.mcursor().position
                localPos = comp.screenToLocal(cursorPos)
                relPos = Math.Vector2(localPos.x / comp.size.x, localPos.y / comp.size.y)
                xCenter, yCenter = parentMap.worldMapAnchor
                minX = xCenter - parentMap.worldMapWidth / 2
                minY = yCenter - parentMap.worldMapHeight / 2
                maxX = xCenter + parentMap.worldMapWidth / 2
                maxY = yCenter + parentMap.worldMapHeight / 2
                markerPosX = minX * (1.0 - relPos.x) + maxX * relPos.x
                markerPosZ = minY * relPos.y + maxY * (1.0 - relPos.y)
                parentMap.sendMarkerMessage(markerPosX, markerPosZ)
        return False


class Minimap(MapBase):
    VR_LINE_COLOR = Math.Vector4(187, 187, 187, 255)
    DEFAULT_ZOOM = 700
    NORMAL_MAP_SIZE = 175.0

    def __init__(self, spaceName, funcMarkerMessageCallBack):
        """
        @param str spaceName:
        @param function funcMarkerMessageCallBack:
        """
        MapBase.__init__(self)
        self._groupEntities = dict()
        self._groupEntitiesData = self._initGroupEntitiesData()
        self._vehicleStepDepth = (MapBase.MIN_ENTRY_DEPTH - MapBase.MAX_ENTRY_DEPTH) / (WAITING_QUEUE_MAX_SIZE + 1)
        self._vehicleEnemyDepth = MapBase.MAX_ENTRY_DEPTH
        self._vehicleAllyDepth = MapBase.MAX_ENTRY_DEPTH + (MapBase.MIN_ENTRY_DEPTH - MapBase.MAX_ENTRY_DEPTH) / 2
        self._vehicleDepthMap = dict()
        self._teamObjectsStepDepth = abs(MapBase.TEAM_OBJECT_DEPTH - MapBase.BASE_OBJECT_DEPTH) / (GAME_OBJECTS_PER_ARENA_LIMIT + 1)
        self._teamObjectsDepthMap = dict()
        self.__funcMarkerMessageCallBack = funcMarkerMessageCallBack
        self.DOMINATION_TEXTURE_OWN = db.DBLogic.g_instance.getGUITexture('TX_HUDMAP_BASE_ALLY')
        self.DOMINATION_TEXTURE_ENEMY = db.DBLogic.g_instance.getGUITexture('TX_HUDMAP_BASE_ENEMY')
        self.spaceName = spaceName
        self._visible = False
        self.map = GUI.Minimap()
        self._prepareVisibilityRangeData()
        self.map.setUIAtlas(MapBase.VR_ATLAS_TEXTURE, MapBase.VR_DESC_ATLAS)
        self.map.materialFX = 'BLEND'
        self.map.widthMode = 'PIXEL'
        self.map.heightMode = 'PIXEL'
        self.map.rotate = False
        self.map.setVisibleRangeColour(Minimap.VR_LINE_COLOR)
        self.map.textureName = db.DBLogic.g_instance.getGUITexture('TX_MAP_DEFAULT')
        self.map.maskName = db.DBLogic.g_instance.getGUITexture('TX_MAP_MASK')
        self.map.simpleEntrySize = 17
        self.map.useUpDown = False
        self.map.range = Minimap.DEFAULT_ZOOM
        self.map.currentRange = self.map.range
        self.map.script = MinimapEventHandler(weakref.ref(self))
        self.map.focus = True
        self.map.mouseButtonFocus = True
        self.map.moveFocus = True
        self.map.crossFocus = True
        self.map.margin = -1.0
        self.map.filterType = 'LINEAR'
        self.map.entityPosInRadarBorder = True
        self.map.widthMode = 'PIXEL'
        self.map.heightMode = 'PIXEL'
        self.map.minEntryDepth = MapBase.MIN_ENTRY_DEPTH
        self.map.maxEntryDepth = MapBase.MAX_ENTRY_DEPTH
        self.background = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAP_DEFAULT'))
        self.background.materialFX = 'BLEND'
        self.background.verticalAnchor = 'BOTTOM'
        self.background.horizontalAnchor = 'RIGHT'
        self.background.widthMode = 'PIXEL'
        self.background.heightMode = 'PIXEL'
        self.background.filterType = 'LINEAR'
        self.mapHolder = GUI.Window('')
        self.mapHolder.verticalPositionMode = 'PIXEL'
        self.mapHolder.horizontalPositionMode = 'PIXEL'
        self.mapHolder.materialFX = 'BLEND'
        self.mapHolder.widthMode = 'PIXEL'
        self.mapHolder.heightMode = 'PIXEL'
        self.mapHolder.verticalAnchor = 'TOP'
        self.mapHolder.horizontalAnchor = 'LEFT'
        self.mapHolder.filterType = 'LINEAR'
        self.foreground = GUI.Window()
        self.foreground.materialFX = 'BLEND'
        self.foreground.widthMode = 'PIXEL'
        self.foreground.heightMode = 'PIXEL'
        self.background.filterType = 'LINEAR'
        self.grid = GUI.Window()
        self.grid.materialFX = 'BLEND'
        self.grid.widthMode = 'CLIP'
        self.grid.heightMode = 'CLIP'
        self.background.filterType = 'LINEAR'
        self.dominationPointsCount = 0
        self.ownDominationTexture = BigWorld.PyTextureProvider(self.DOMINATION_TEXTURE_OWN)
        self.enemyDominationTexture = BigWorld.PyTextureProvider(self.DOMINATION_TEXTURE_ENEMY)
        self.dominationPoints = None
        self.boundTextureV = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_BOUND_TEXTURE_V'))
        self.boundsEnable = False
        self.__eventManager = EventManager()
        self.eMinimapResized = Event(self.__eventManager)
        self.__limitPosition = Math.Vector2(0.0, 0.0)
        self.__mapSize = Settings.g_instance.getGameUI()['minimapSize']
        self._constructLayers()
        self.setVisible(False)
        return

    def _initGroupEntitiesData(self):
        groupEntitiesData = list()
        groupEntitiesData.append('')
        for i in range(1, MapBase.GROUPS_MARKERS_COUNT):
            groupEntitiesData.append(db.DBLogic.g_instance.getGUITexture(MapBase.GROUPS_MARKERS_TEXTURE_ID % str(i)))

        return groupEntitiesData

    def _prepareVisibilityRangeData(self):
        self.map.setVisibilityRangeData(VisibilityRangeType.ONE_TEXTURE_ONE_MESH, MapBase.VR_SECTOR_TEXTURE, MapBase.VR_OVERLAY_TEXTURE, MapBase.VR_MASK_TEXTURE, MapBase.VR_DIRECTION_LINE_COLOR, True)

    def destroy(self):
        self._groupEntities.clear()
        self.__funcMarkerMessageCallBack = None
        self.__eventManager.clear()
        MapBase.destroy(self)
        return

    def _constructLayers(self):
        self.__loadMapData()
        self.__updateMapSize()
        self.mapHolder.addChild(self.map, 'map')
        self.background.addChild(self.mapHolder, 'mapholder')
        self.background.addChild(self.foreground, 'foreground')
        self.background.addChild(self.grid, 'grid')

    def __loadMapData(self):
        self.__mapSettings = {}
        for key, data in ResMgr.openSection('gui/minimap_sizes.xml').items():
            if key == 'size':
                setting = {}
                setting['id'] = data.readInt('id')
                setting['offset'] = data.readVector2('offset', (0, 0))
                setting['gridTexture'] = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture(data.readString('texture_grid')))
                setting['overlayTexture'] = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture(data.readString('texture_overlay')))
                setting['texture'] = BigWorld.PyTextureProvider(self.spaceName + db.DBLogic.g_instance.getGUITexture(data.readString('texture_map')))
                setting['mapPosition'] = data.readVector3('map_position')
                setting['mapSize'] = data.readVector2('map_size')
                self.__mapSettings[setting['id']] = setting
            else:
                LOG_WARNING('gui/minimap_sizes.xml containg unexpected section: [%s]', key)

        ResMgr.purge('gui/minimap_sizes.xml')

    @noexcept
    def __updateMapSize(self):
        data = [ val for key, val in self.__mapSettings.items() if key == self.__mapSize ]
        if not data:
            LOG_ERROR('Specified minimap size [%s] not found!' % self.__mapSize)
        data = data[0]
        self.background.horizontalPositionMode = 'LEGACY'
        self.background.verticalPositionMode = 'LEGACY'
        self.setDepth(GUI_COMPONENTS_DEPH.MINIMAP_IN_BATTLE_LOADING if not GameEnvironment.getHUD().isTutorial() else GUI_COMPONENTS_DEPH.MINIMAP_IN_HUD, False)
        self.background.size = (data['overlayTexture'].width, data['overlayTexture'].height)
        self.foreground.size = (data['overlayTexture'].width, data['overlayTexture'].height)
        self.foreground.verticalAnchor = 'TOP'
        self.foreground.horizontalAnchor = 'LEFT'
        self.foreground.verticalPositionMode = 'PIXEL'
        self.foreground.horizontalPositionMode = 'PIXEL'
        self.foreground.position = (data['offset'][0], data['offset'][1], 0)
        self.foreground.texture = data['overlayTexture']
        self.grid.widthMode = 'PIXEL'
        self.grid.heightMode = 'PIXEL'
        self.grid.size = (data['gridTexture'].width, data['gridTexture'].height)
        self.grid.verticalAnchor = 'TOP'
        self.grid.horizontalAnchor = 'LEFT'
        self.grid.verticalPositionMode = 'PIXEL'
        self.grid.horizontalPositionMode = 'PIXEL'
        self.grid.position = (data['offset'][0], data['offset'][1], 0)
        self.grid.texture = data['gridTexture']
        self.mapHolder.position = (data['mapPosition'][0] + data['offset'][0], data['mapPosition'][1] + data['offset'][1], 0)
        self.mapHolder.size = data['mapSize']
        self.mapHolder.texture = data['texture']
        self.map.position = (0.0, 0.0, 0.0)
        self.map.size = data['mapSize']

    def getMapSize(self):
        return self.__mapSize

    def setDepth(self, newDepth, isResort):
        self.background.position = (1, -1, newDepth)
        if isResort:
            GUI.reSort()

    def setVisibleTeamObjects(self, isVisible):
        for entityObject in self._entityObject.itervalues():
            if entityObject[1] in [HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT, HUD_MINIMAP_ENTITY_TYPE_TURRET, HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE]:
                entityObject[0].visible = isVisible

    def setAltState(self, isFired):
        MapBase.setAltState(self, isFired)
        if SUPERIORITY2_BASE_HEALTH:
            self._updateGroupEntitiesVisibility(isFired)
            self.setVisibleTeamObjects(isFired)
            self._updateLockTargetVisibility(isFired)

    def _updateGroupEntitiesVisibility(self, isVisible):
        for pComponent in self._groupEntities.itervalues():
            if pComponent.textureName:
                pComponent.visible = not isVisible

    def _updateLockTargetVisibility(self, isVisible):
        lockTargetID = self._lockTargetData.get('entityID', None)
        if lockTargetID is not None:
            entityObject = self._entityObject.get(lockTargetID, None)
            if entityObject is not None:
                if entityObject[1] in [HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT, HUD_MINIMAP_ENTITY_TYPE_TURRET, HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE]:
                    self._setVisibleLocked(isVisible)
        return

    def setEntityText(self, entity, text):
        mapId = self.entities.get(entity.id, None)
        if mapId is not None:
            self.map.setEntityText(mapId, text)
        else:
            LOG_DEBUG('setEntityText - entity not in self.entities', entity.id, text)
        return

    def setMapSize(self, sz):
        """ sz could be one of the specified in [gui/minimap_sizes.xml] """
        scaleCfc = sz / float(self.__mapSize)
        self.__mapSize = sz
        self.__updateMapSize()
        self.notifySizeChange()
        for mapId in self.entities.values():
            self.__resizeComponent(mapId, scaleCfc)

        self._resizeLocked()

    def __resizeComponent(self, mapId, scaleCfc):
        entityComponent = self.map.getEntityComponent(mapId)
        if entityComponent:
            entityComponent.size.x *= scaleCfc
            entityComponent.size.y *= scaleCfc

    def _resizeLocked(self):
        lockTargetID = self._lockTargetData.get('ID', None)
        if lockTargetID is not None:
            entityComponent = self.map.getEntityComponent(lockTargetID)
            entityComponent.size = self._getResContainer().ENTITY_COMPONENTS[self._state][self._entityObject[self._lockTargetData.get('entityID')][1]][self.ENTITY_LOCKED]['size']
            self.__resizeComponent(lockTargetID, float(self.__mapSize) / Minimap.NORMAL_MAP_SIZE)
        return

    def setLocked(self, entity, isLocked):
        MapBase.setLocked(self, entity, isLocked)
        if SUPERIORITY2_BASE_HEALTH:
            self._updateLockTargetVisibility(isLocked and self._state == 1)
        self._resizeLocked()

    def __getScreenPosInPixel(self, component):
        """
        @param component: SimpleGUIComponent
        @return: Vector2
        """
        posInScreen = self.map.localToScreen(Math.Vector2(component.position.x, component.position.y))
        return Math.Vector2(BigWorld.screenWidth() * (posInScreen.x + 1) / 2, BigWorld.screenHeight() * (-posInScreen.y + 1) / 2)

    def __checkIncMapSize(self, sz):
        sizeData = self.__mapSettings.get(sz, None)
        if sizeData is not None:
            nextSize = Math.Vector2(sizeData['overlayTexture'].width, sizeData['overlayTexture'].height)
            prevPos = self.__getScreenPosInPixel(self.background)
            prevPos.x = prevPos.x - sizeData['offset'][0]
            prevPos.y = prevPos.y - sizeData['offset'][1]
            nextPos = Math.Vector2(prevPos.x - (nextSize.x - self.background.size.x), prevPos.y - (nextSize.y - self.background.size.y))
            if self.__limitPosition.x < nextPos.x and self.__limitPosition.y < nextPos.y:
                return True
        return False

    def incMapSize(self):
        nextSet = [ key for key in self.__mapSettings.keys() if key > self.__mapSize ]
        if nextSet:
            sz = min(nextSet)
            if not self.__checkIncMapSize(sz):
                return
            self.setMapSize(sz)
        Settings.g_instance.getGameUI()['minimapSize'] = self.__mapSize

    def decMapSize(self):
        nextSet = [ key for key in self.__mapSettings.keys() if key < self.__mapSize ]
        if nextSet:
            self.setMapSize(max(nextSet))
        Settings.g_instance.getGameUI()['minimapSize'] = self.__mapSize

    @noexcept
    def notifySizeChange(self):
        data = [ val for key, val in self.__mapSettings.items() if key == self.__mapSize ]
        if not data:
            LOG_ERROR('Specified minimap size [%s] not found!' % self.__mapSize)
        data = data[0]
        self.eMinimapResized(self.foreground.size.y - data['offset'][1])

    @staticmethod
    def getPreloadedResources():
        return MapBase._getPreloadedResources(db.DBLogic.g_instance.getNavigationWindowData(NAVIGATION_WINDOWS_TYPES.MINIMAP).container)

    def setBounds(self, bounds):
        LOG_DEBUG('BOUND!!!!', bounds)
        if self.boundsEnable:
            LOG_ERROR('Bound already enabled')
        if len(bounds) > 1:
            self.boundsEnable = True
            left = 10000000000.0
            right = -10000000000.0
            top = 10000000000.0
            bottom = -10000000000.0
            for point in bounds:
                left = min(left, point.x)
                right = max(right, point.x)
                top = min(top, point.z)
                bottom = max(bottom, point.z)

            self.map.setWorldSize((left, bottom), (right, top))
            self.worldMapWidth = right - left
            self.worldMapHeight = -(top - bottom)
            xCenter = left + self.worldMapWidth / 2.0
            yCenter = bottom + -self.worldMapHeight / 2.0
            curSizeMax = self.worldMapHeight
            if self.worldMapWidth > curSizeMax:
                curSizeMax = self.worldMapWidth
            self.map.range = curSizeMax / 2
            self.map.currentRange = self.map.range
            self.map.ratioX = self.worldMapWidth / curSizeMax
            self.map.ratioY = self.worldMapHeight / curSizeMax
            self.map.viewpoint = BigWorld.VectorOffsetProvider(Math.Vector3(xCenter, 0.0, yCenter))
            self.worldMapAnchor = (xCenter, yCenter)
            self.__initGridPosition()
            self._updateTexture()

    def _updateTexture(self):
        pass

    def refreshDominationPoints(self):
        if self.dominationPoints is not None:
            self.setDominationPoint(self.dominationPoints)
        return

    def __addDominationArrow(self, point):
        matrix = Math.Matrix()
        matrix.setTranslate(Math.Vector3(point[0], point[1], point[2]))

    def setDominationPoint(self, points):
        for i in range(MapBase.DOMITATION_LAYER, self.dominationPointsCount + MapBase.DOMITATION_LAYER):
            self.map.delTextureLayer(i)

        player = BigWorld.player()
        self.dominationPointsCount = 0
        self.dominationPoints = points
        for point in points:
            texture = self.ownDominationTexture
            if self.dominationPointsCount != player.teamIndex:
                self.__addDominationArrow(point)
                texture = self.enemyDominationTexture
            size = (self.worldMapWidth / self.map.size.x * 8.0, self.worldMapHeight / self.map.size.y * -8.0)
            pos = (point[0], point[2])
            self.map.addTextureLayer(self.dominationPointsCount + MapBase.DOMITATION_LAYER, texture, size, pos)
            self.dominationPointsCount += 1

    def add(self, entity):
        guiId = self.entities.get(entity.id, None)
        if guiId is not None:
            self.map.setMatrix(guiId, entity.mapMatrix)
            self.map.setVisibility(guiId, self._checkVisibilityBeforeAdd(entity))
        else:
            c = self.getEntityGUI('', MapBase.FRIEND_COLOR)
            entityType, entityState, upTexture, lock = MapBase.setupComponent(self, entity, c, False)
            self._correctionComponentsSize(c)
            c.position = self._getEntityDepth(entity, entityType)
            self.entities[entity.id] = self.map.add(entity.mapMatrix, c, '', lock, True)
            MapBase.add(self, entity, c, entityType, entityState)
        return

    def _checkVisibilityBeforeAdd(self, entity):
        if not SUPERIORITY2_BASE_HEALTH:
            return True
        return self._isAvatar(entity)

    def _correctionComponentsSize(self, c):
        """
        correction component size
        @param c: <SimpleGUIComponent>
        """
        c.size.x *= self.__mapSize / 100.0
        c.size.y *= self.__mapSize / 100.0

    def _getEntityDepth(self, entity, entityType):
        """
        @param entity:
        @param entityType: HUD_MINIMAP_ENTITY_TYPE_AVATAR, HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT, ...
        @return: Vector3 - entity position
        """
        player = BigWorld.player()
        if entity is player:
            return Math.Vector3(0, 0, MapBase.PLAYER_DEPTH)
        elif self._isAvatar(entity):
            if entity.id not in self._vehicleDepthMap:
                if entity.teamIndex == player.teamIndex:
                    depth = self._vehicleAllyDepth
                    self._vehicleAllyDepth += self._vehicleStepDepth
                else:
                    depth = self._vehicleEnemyDepth
                    self._vehicleEnemyDepth += self._vehicleStepDepth
                self._vehicleDepthMap[entity.id] = depth
            return Math.Vector3(0, 0, self._vehicleDepthMap[entity.id])
        elif entityType == HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE:
            return Math.Vector3(0, 0, MapBase.BASE_OBJECT_DEPTH)
        else:
            if entity.id not in self._teamObjectsDepthMap:
                self._teamObjectsDepthMap[entity.id] = MapBase.TEAM_OBJECT_DEPTH + self._teamObjectsStepDepth * len(self._teamObjectsDepthMap)
            return Math.Vector3(0, 0, self._teamObjectsDepthMap[entity.id])

    def removeAllMarkers(self):
        """
        Remove all markers from minimap
        """
        self.map.removeAllMarkers()

    def _updateGUIVisibility(self, isVisible):
        if isVisible:
            GUI.addRoot(self.background)
        else:
            self.map.removeAllMarkers()
            GUI.delRoot(self.background)

    def sendMarkerMessage(self, posX, posZ):
        self.__funcMarkerMessageCallBack(posX, posZ)

    def getGridPosition(self, posX, posZ):
        posGridX = self.__gridPositionsWidth[int(abs((min(posX, self.__maxX - 1) - self.__minX) / self.__stepX))]
        posGridZ = self.__gridPositionsHeight[int(abs((min(posZ, self.__maxY - 1) - self.__minY) / self.__stepY))]
        return (posGridX, posGridZ)

    def __initGridPosition(self):
        self.__gridPositionsWidth = ['1',
         '2',
         '3',
         '4',
         '5',
         '6',
         '7',
         '8',
         '9',
         '0']
        self.__gridPositionsHeight = ['K',
         'J',
         'H',
         'G',
         'F',
         'E',
         'D',
         'C',
         'B',
         'A']
        xCenter, yCenter = self.worldMapAnchor
        self.__minX = xCenter - self.worldMapWidth / 2
        self.__minY = yCenter - self.worldMapHeight / 2
        self.__maxX = xCenter + self.worldMapWidth / 2
        self.__maxY = yCenter + self.worldMapHeight / 2
        self.__stepX = (self.__maxX + abs(self.__minX)) / len(self.__gridPositionsWidth)
        self.__stepY = (self.__maxY + abs(self.__minY)) / len(self.__gridPositionsHeight)

    def setLimitPosition(self, posX, posY):
        self.__limitPosition.x = posX
        self.__limitPosition.y = posY
        if not self.__checkIncMapSize(self.__mapSize):
            for sz in self.__mapSettings.iterkeys():
                if sz < self.__mapSize and self.__checkIncMapSize(sz):
                    self.setMapSize(sz)
                    return

            self.setMapSize(min(self.__mapSettings.iterkeys()))

    def _getResContainer(self):
        return db.DBLogic.g_instance.getNavigationWindowData(NAVIGATION_WINDOWS_TYPES.MINIMAP).container

    def setVisibility(self, entity, isVisible):
        guiId = self.entities.get(entity.id, None)
        if guiId is not None:
            self.map.setVisibility(guiId, isVisible and self._checkVisibilityBeforeAdd(entity))
        return

    def addGroup(self, groupName, groupEntities):
        pComponent = self.getEntityGUI(self._groupEntitiesData[0], MapBase.PLAYER_COLOR)
        pComponent.position.z = MapBase.TEAM_OBJECT_DEPTH - self._teamObjectsStepDepth * len(self._groupEntities)
        if groupName not in self._groupEntities:
            self._groupEntities[groupName] = pComponent
        group = list()
        for entityID in groupEntities:
            mapID = self.entities.get(entityID, None)
            if mapID is not None:
                group.append(mapID)

        self.map.addEntitiesGroup(groupName, tuple(group), pComponent)
        self.setVisibilityGroup(groupName, False)
        return

    def initGroup(self, groupName, iconIndex):
        if iconIndex > len(self._groupEntitiesData) - 1:
            LOG_DEBUG('initGroup - iconIndex out of range', groupName, iconIndex)
            return
        elif iconIndex == 0:
            self.setVisibilityGroup(groupName, False)
            return
        else:
            self.map.setLockRotationEntitiesGroup(groupName, iconIndex not in MapBase.GROUPS_MARKERS_WITH_ROTATION)
            pComponent = self._groupEntities.get(groupName, None)
            if pComponent is not None:
                pComponent.textureName = self._groupEntitiesData[iconIndex]
                self.setVisibilityGroup(groupName, True)
            return

    def setVisibilityGroup(self, groupName, isVisible):
        self.map.setVisibilityEntitiesGroup(groupName, isVisible and SUPERIORITY2_BASE_HEALTH)