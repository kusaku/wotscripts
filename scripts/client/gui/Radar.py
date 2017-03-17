# Embedded file name: scripts/client/gui/Radar.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import ResMgr
import Math
from MathExt import clamp
from functools import partial
from MapBase import *
from HUDconsts import *
from debug_utils import LOG_DEBUG
import Settings
from consts import NAVIGATION_WINDOWS_TYPES

class Radar(MapBase):
    BOUNDS_COLOR_STATES = [4293340462L, 4282990028L]
    BOUNDS_LAYER = 20
    BOUND_THICKNESS = 8.0
    ZOOM_STEP = 100.0
    ZOOM_MAX = 1200.0
    ZOOM_MIN = 125.0
    DEFAULT_ZOOM = 250.0
    ENTITY_MAX_SIZE = 2.0
    ENTITY_SIZE_MAX_ALT = 500.0 / 6.0
    GRID_COLOUR = (187, 187, 187, 200)
    VISIBLE_RANGE_COLOUR = (187, 187, 187, 0)
    SIZE = 220

    def __init__(self, spaceName):
        MapBase.__init__(self)
        self.spaceName = spaceName
        self.map = GUI.Minimap()
        self._prepareVisibilityRangeData()
        self.map.setUIAtlas(MapBase.VR_ATLAS_TEXTURE, MapBase.VR_DESC_ATLAS)
        self.map.materialFX = 'BLEND'
        self.map.widthMode = 'PIXEL'
        self.map.heightMode = 'PIXEL'
        self.map.rotate = False
        self.map.size = (Radar.SIZE, Radar.SIZE)
        self.map.position = (0, 0, 1.0)
        self.map.textureName = db.DBLogic.g_instance.getGUITexture('TX_MAP_DEFAULT')
        self.map.simpleEntryMap = db.DBLogic.g_instance.getGUITexture('TX_MINIMAP_PLAYER')
        self.map.simpleEntrySize = 17
        self.map.useUpDown = False
        self.map.range = Settings.g_instance.getGameUI()['navigationWindowRange']
        self.map.staticRange = Radar.ZOOM_MIN
        self.map.margin = 0.15
        self.map.drawGrid = False
        self.map.entityPosInRadarBorder = True
        self.map.enityMaxResize = self.ENTITY_MAX_SIZE
        self.map.maxEntityHeight = self.ENTITY_SIZE_MAX_ALT
        self.dominationPointsCount = 0
        self.ownDominationTexture = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_DOMINATION_TEXTURE_OWN'))
        self.enemyDominationTexture = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_DOMINATION_TEXTURE_ENEMY'))
        self.dominationPoints = None
        self.boundTextureV = BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_BOUND_TEXTURE_V'))
        self.boundsEnable = False
        self.direction = GUI.MatrixProvider(db.DBLogic.g_instance.getGUITexture('HUD_RADAR_PLANE_LINE'))
        self.direction.materialFX = 'BLEND'
        self.direction.widthMode = 'PIXEL'
        self.direction.heightMode = 'PIXEL'
        self.direction.size = (19, Radar.SIZE)
        self.direction.position = (0, 0, 0.99)
        self.overlay = GUI.MatrixProvider(db.DBLogic.g_instance.getGUITexture('TX_RADAR_OVERLAY_TEXTURE'))
        self.overlay.materialFX = 'BLEND'
        self.overlay.widthMode = 'PIXEL'
        self.overlay.heightMode = 'PIXEL'
        self.overlay.size = (Radar.SIZE, Radar.SIZE)
        self.overlay.position = (0, 0, 0)
        self.background = GUI.Window(db.DBLogic.g_instance.getGUITexture('HUD_RADAR_BG'))
        self.background.materialFX = 'BLEND'
        self.background.verticalAnchor = 'BOTTOM'
        self.background.horizontalAnchor = 'RIGHT'
        self.background.widthMode = 'PIXEL'
        self.background.heightMode = 'PIXEL'
        self.background.verticalPositionMode = 'PIXEL'
        self.background.horizontalPositionMode = 'PIXEL'
        self.background.size = (Radar.SIZE, Radar.SIZE)
        self.updatePosition()
        self.map.maskName = 'gui/maps/hudRadarMask.dds'
        self.background.addChild(self.map, 'map')
        self.map.addChild(self.direction, 'direction')
        if self._visible:
            GUI.addRoot(self.background)
        return

    def _prepareVisibilityRangeData(self):
        self.map.setVisibilityRangeData(VisibilityRangeType.ONE_TEXTURE_TWO_MESHES, MapBase.VR_SECTOR_TEXTURE, MapBase.VR_OVERLAY_TEXTURE, MapBase.VR_MASK_TEXTURE, MapBase.VR_DIRECTION_LINE_COLOR, False)

    @staticmethod
    def getPreloadedResources():
        return MapBase._getPreloadedResources(db.DBLogic.g_instance.getNavigationWindowData(NAVIGATION_WINDOWS_TYPES.RADAR).container)

    def zoomIn(self):
        self.map.range = clamp(Radar.ZOOM_MIN, self.map.range - Radar.ZOOM_STEP, Radar.ZOOM_MAX)
        Settings.g_instance.setGameUIValue('navigationWindowRange', self.map.range)

    def zoomOut(self):
        self.map.range = clamp(Radar.ZOOM_MIN, self.map.range + Radar.ZOOM_STEP, Radar.ZOOM_MAX)
        Settings.g_instance.setGameUIValue('navigationWindowRange', self.map.range)

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

            vSize = (Radar.BOUND_THICKNESS, bottom - top)
            hSize = (right - left, Radar.BOUND_THICKNESS)
            vCenter = (bottom + top) / 2.0
            hCenter = (right + left) / 2.0
            self.map.setWorldSize((left, bottom), (right, top))
            self.map.showBounds(3.0, Radar.BOUNDS_COLOR_STATES[int(Settings.g_instance.getGameUI()['alternativeColorMode'])])

    def setState(self, val):
        MapBase.setState(self, val)
        self.map.showBounds(3.0, Radar.BOUNDS_COLOR_STATES[val])

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
            size = (point[3] * 2.0, point[3] * 2.0)
            pos = (point[0], point[2])
            self.map.addTextureLayer(self.dominationPointsCount + MapBase.DOMITATION_LAYER, texture, size, pos)
            self.dominationPointsCount += 1

    def add(self, entity):
        if self._isAvatar(entity):
            guiId = self.entities.get(entity.id, None)
            if guiId is not None:
                self.map.setMatrix(guiId, entity.mapMatrix)
                self.map.setVisibility(guiId, True)
            else:
                color = MapBase.FRIEND_COLOR
                player = BigWorld.player()
                if entity.teamIndex != player.teamIndex:
                    color = MapBase.ENEMY_COLOR
                if entity is player:
                    self.direction.source = entity.mapMatrix
                    self.map.setDirectionComponent(entity.mapMatrix, self.direction)
                elif self.map.useUpDown:
                    up = self.getEntityGUI(db.DBLogic.g_instance.getGUITexture('TX_MINIMAP_ENTITY_UP'), color)
                    down = self.getEntityGUI(db.DBLogic.g_instance.getGUITexture('TX_MINIMAP_ENTITY_DOWN'), color)
                    self.entities[entity.id] = self.map.addUpDown(entity.mapMatrix, up, down)
                else:
                    c = self.getEntityGUI('', color)
                    entityType, enityState, upTexture, lock = MapBase.setupComponent(self, entity, c, False)
                    self.entities[entity.id] = self.map.add(entity.mapMatrix, c, upTexture, lock, False)
                    MapBase.add(self, entity, c, entityType, enityState)
        return

    def getEntityGUI(self, path, color):
        c = MapBase.getEntityGUI(self, path, color)
        c.size = (24, 24)
        return c

    def _updateGUIVisibility(self, isVisible):
        if isVisible:
            GUI.addRoot(self.background)
        else:
            GUI.delRoot(self.background)

    def updatePosition(self):
        """
        update radar position in pixels
        """
        gameUI = Settings.g_instance.getGameUI()
        hPos = gameUI['radarPosX'] if 'radarPosX' in gameUI else HUD_RADAR_POSITION[0]
        vPos = gameUI['radarPosY'] if 'radarPosY' in gameUI else HUD_RADAR_POSITION[1]
        self.background.position = Math.Vector3(hPos, vPos + Radar.SIZE, HUD_RADAR_POSITION[2])

    def setSpectatorMode(self, isSpectatorMode):
        self.direction.visible = not isSpectatorMode

    def setEntityCommand(self, senderID, pMatrix, commandID):
        pass

    def _getResContainer(self):
        return db.DBLogic.g_instance.getNavigationWindowData(NAVIGATION_WINDOWS_TYPES.RADAR).container