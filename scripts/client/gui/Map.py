# Embedded file name: scripts/client/gui/Map.py
import BigWorld
import GUI
import GameEnvironment
import Helpers.PyGUI as PyGUI
import ResMgr
import Math
from MathExt import clamp
from HUDconsts import HUD_MAXIMAP_SIZE, HUD_MAXIMAP_BORDER_SIZE, HUD_MAXIMAP_CLOSEBUTTON_SIZE, HUD_MAXIMAP_FOREGROUND_SIZE, HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE, HUD_MAXIMAP_BACKGROUND_SIZE
from MapBase import *
from Minimap import Minimap
import gui.hud
import InputMapping
import weakref
import Keys
from consts import NAVIGATION_WINDOWS_TYPES
from consts import SUPERIORITY2_BASE_HEALTH

class CloseBtEventHandler:

    def __init__(self, parent):
        pass

    def handleMouseButtonEvent(self, comp, event):
        if event.isKeyUp():
            cmdMap = InputMapping.g_instance
            commandProcessor = GameEnvironment.getInput().commandProcessor
            commandShowMap = commandProcessor.getCommand(InputMapping.CMD_SHOW_MAP)
            commandShowMap.isFired = False
            GameEnvironment.getHUD().showMap(False, [], not GameEnvironment.getInput().isFired(InputMapping.CMD_SHOW_CURSOR))
        return False

    def handleMouseEnterEvent(self, comp):
        comp.textureName = db.DBLogic.g_instance.getGUITexture('TX_MAXIMAP_CLOSE_OVER')
        return False

    def handleMouseLeaveEvent(self, comp):
        comp.textureName = db.DBLogic.g_instance.getGUITexture('TX_MAXIMAP_CLOSE_UP')
        return False


class Map(Minimap):

    def __init__(self, spaceName, funcMarkerMessageCallBack):
        """
        @param str spaceName:
        @param function funcMarkerMessageCallBack:
        """
        Minimap.__init__(self, spaceName, funcMarkerMessageCallBack)

    def _constructLayers(self):
        mapSize = HUD_MAXIMAP_SIZE
        borderSize = HUD_MAXIMAP_BORDER_SIZE
        closeBtSize = HUD_MAXIMAP_CLOSEBUTTON_SIZE
        self.map.position = (0.0, 0.0, 0.0)
        self.map.size = (mapSize - borderSize * 2, mapSize - borderSize * 2)
        self.mapHolder.verticalAnchor = 'CENTER'
        self.mapHolder.horizontalAnchor = 'CENTER'
        self.mapHolder.verticalPositionMode = 'CLIP'
        self.mapHolder.horizontalPositionMode = 'CLIP'
        self.mapHolder.position = (0.0, 0.0, 0.0)
        self.mapHolder.size = (HUD_MAXIMAP_BACKGROUND_SIZE, HUD_MAXIMAP_BACKGROUND_SIZE)
        self.background.verticalPositionMode = 'PIXEL'
        self.background.horizontalPositionMode = 'PIXEL'
        self.background.verticalAnchor = 'TOP'
        self.background.horizontalAnchor = 'LEFT'
        self.background.position = (0.0, 0.0, 0.0)
        self.background.widthMode = 'CLIP'
        self.background.heightMode = 'CLIP'
        self.background.size = (2.0, 2.0)
        self.background.textureName = db.DBLogic.g_instance.getGUITexture('TX_MAXIMAP_BG')
        self.mapHolder.addChild(self.map, 'map')
        self.background.addChild(self.mapHolder, 'mapholder')
        self.closeBt = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAXIMAP_CLOSE_UP'))
        self.closeBt.widthMode = 'PIXEL'
        self.closeBt.heightMode = 'PIXEL'
        self.closeBt.verticalAnchor = 'CENTER'
        self.closeBt.horizontalAnchor = 'CENTER'
        self.closeBt.verticalPositionMode = 'PIXEL'
        self.closeBt.horizontalPositionMode = 'PIXEL'
        self.closeBt.size = (closeBtSize, closeBtSize)
        self.closeBt.position = (mapSize + closeBtSize / 2, borderSize + closeBtSize / 2, 0.0)
        self.closeBt.script = CloseBtEventHandler(weakref.ref(self))
        self.closeBt.mouseButtonFocus = True
        self.closeBt.focus = True
        self.closeBt.crossFocus = True
        self.foreground = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAP_OVERLAY_TEXTURE'))
        self.foreground.materialFX = 'BLEND'
        self.foreground.widthMode = 'PIXEL'
        self.foreground.heightMode = 'PIXEL'
        self.foreground.size = (HUD_MAXIMAP_FOREGROUND_SIZE, HUD_MAXIMAP_FOREGROUND_SIZE)
        self.foreground.position = (0.0, 0.0, 0.0)
        self.background.addChild(self.foreground, 'foreground')

    def _prepareVisibilityRangeData(self):
        self.map.setVisibilityRangeData(VisibilityRangeType.ONE_TEXTURE_ONE_MESH, MapBase.VR_SECTOR_TEXTURE, MapBase.VR_OVERLAY_TEXTURE, MapBase.VR_MASK_TEXTURE, MapBase.VR_DIRECTION_LINE_COLOR, True)

    def _updateTexture(self):
        self.textureName = self.spaceName + db.DBLogic.g_instance.getGUITexture('TX_MAP_TEXTURE')
        BigWorld.loadResourceListBG((self.textureName,), self._onLoadTexture)

    def _onLoadTexture(self, resourceRef):
        mapTexture = resourceRef[self.textureName]
        self.mapHolder.texture = mapTexture

    @staticmethod
    def getPreloadedResources():
        return MapBase._getPreloadedResources(db.DBLogic.g_instance.getNavigationWindowData(NAVIGATION_WINDOWS_TYPES.BIG_MAP).container)

    def getEntityGUI(self, path, color):
        c = GUI.Simple(path)
        c.materialFX = 'BLEND'
        c.widthMode = 'PIXEL'
        c.heightMode = 'PIXEL'
        c.size = (32, 32)
        c.filterType = 'LINEAR'
        return c

    def setAltState(self, isFired):
        MapBase.setAltState(self, isFired)

    def _checkVisibilityBeforeAdd(self, entity):
        return True

    def setVisibility(self, entity, isVisible):
        MapBase.setVisibility(self, entity, isVisible)

    def _updateAltState(self):
        if not SUPERIORITY2_BASE_HEALTH:
            MapBase._updateAltState(self)
            return
        else:
            for id, entityObject in self._entityObject.items():
                if id != BigWorld.player().id:
                    entity = entityObject[1]
                    if entity in [HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT, HUD_MINIMAP_ENTITY_TYPE_TURRET, HUD_MINIMAP_ENTITY_TYPE_TEAM_OBJECT_BASE]:
                        if id in self.entities:
                            objType = GameEnvironment.getHUD().getTeamObjectTypeByParts(id)
                            if objType is not None and objType in MapBase.ALT_STATES_TEAM_OBJECTS:
                                state = MapBase.ALT_STATES_TEAM_OBJECTS[objType]
                                if state in self.ENTITY_COMPONENTS:
                                    entityComponent = self.map.getEntityComponent(self.entities[id])
                                    if entityComponent:
                                        entityComponent.textureName = self.ENTITY_COMPONENTS[state][entity][entityObject[2]]['texture']
                                else:
                                    LOG_ERROR('_updateAltState - state(%s) not in ENTITY_COMPONENTS' % state)
                            else:
                                LOG_ERROR('_updateAltState - objType(%s) not in ALT_STATES_TEAM_OBJECTS' % objType)
                        else:
                            LOG_ERROR('_updateAltState - id(%s) not in self.entities' % id)

            return

    def _correctionComponentsSize(self, c):
        pass

    def setLocked(self, entity, isLocked):
        MapBase.setLocked(self, entity, isLocked)

    def _getResContainer(self):
        return db.DBLogic.g_instance.getNavigationWindowData(NAVIGATION_WINDOWS_TYPES.BIG_MAP).container

    def setAltState(self, isFired):
        MapBase.setAltState(self, isFired)
        self.map.entityTextVisible = isFired