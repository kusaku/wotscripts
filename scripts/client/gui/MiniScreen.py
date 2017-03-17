# Embedded file name: scripts/client/gui/MiniScreen.py
import GUI
import BigWorld
import math
import GameEnvironment
import Math
from MathExt import toVec4
from consts import WORLD_SCALING, TEAM_OBJECT_CLASS_NAMES, AVATAR_CLASS_NAMES
from HUDconsts import *
import Settings
from debug_utils import LOG_DEBUG
from Event import Event
import db.DBLogic

class MiniScreenBase:
    SIZE = (217, 180)

    def __init__(self, mirror):
        self.__visible = False
        self._matrixProvider = None
        self._mirror = mirror
        self._initMatrixProvider()
        self.camera = BigWorld.FreeCamera()
        self.camera.fixed = 1
        self.camera.invViewProvider = self._matrixProvider
        self._sceneRenderer = BigWorld.PyMiniScreenRenderer(MiniScreenBase.SIZE[0] * 2, MiniScreenBase.SIZE[1] * 2)
        self._sceneRenderer.fov = math.radians(self._getFov())
        self._sceneRenderer.cameras = [self.camera]
        self._sceneRenderer.dynamic = 0
        self._sceneRenderer.target = None
        self._guiComponent = GUI.MiniScreenHDR('')
        self._guiComponent.verticalAnchor = 'BOTTOM'
        self._guiComponent.horizontalAnchor = 'LEFT'
        self._guiComponent.widthMode = 'PIXEL'
        self._guiComponent.heightMode = 'PIXEL'
        self._guiComponent.verticalPositionMode = 'PIXEL'
        self._guiComponent.horizontalPositionMode = 'PIXEL'
        if self._mirror:
            self._guiComponent.size = (-MiniScreenBase.SIZE[0], MiniScreenBase.SIZE[1])
        else:
            self._guiComponent.size = (MiniScreenBase.SIZE[0], MiniScreenBase.SIZE[1])
        self._guiComponent.materialFX = 'BLEND'
        self._guiComponent.texture = self._sceneRenderer.texture
        self._guiComponent.setBackground(BigWorld.PyTextureProvider(db.DBLogic.g_instance.getGUITexture('TX_TARGET_BACKGROUND')))
        self._guiComponent.visible = 0
        self.updatePosition()
        GUI.addRoot(self._guiComponent)
        return

    def updatePosition(self):
        settingsUI = Settings.g_instance.getGameUI()
        verticalPosition = settingsUI['MiniScreenPosY'] if 'MiniScreenPosY' in settingsUI else HUD_MINISCREEN_TARGET_INFO[1]
        gorizontalPosition = settingsUI['MiniScreenPosX'] if 'MiniScreenPosX' in settingsUI else HUD_MINISCREEN_TARGET_INFO[0]
        if verticalPosition < 0.0:
            verticalPosition = verticalPosition + BigWorld.screenHeight()
        if self._mirror:
            self._guiComponent.position = Math.Vector3(MiniScreenBase.SIZE[0] + gorizontalPosition - 1, verticalPosition, HUD_MINISCREEN_TARGET_INFO[2])
        else:
            self._guiComponent.position = Math.Vector3(gorizontalPosition - 1, verticalPosition, HUD_MINISCREEN_TARGET_INFO[2])

    def setEntitiesHUD(self, entitiesHUD):
        self._sceneRenderer.entitiesHUD = entitiesHUD

    def _initMatrixProvider(self):
        pass

    def _getFov(self):
        pass

    def update(self):
        pass

    def setVisible(self, flag):
        self.__visible = flag
        if self.__visible and self._sceneRenderer.target and not self._sceneRenderer.target.isDestroyed and self._sceneRenderer.target.inWorld:
            self._guiComponent.visible = 1
            self._sceneRenderer.dynamic = 1
        else:
            self._sceneRenderer.dynamic = 0
            self._guiComponent.visible = 0

    def _isVisible(self):
        return self.__visible

    def destroy(self):
        GUI.delRoot(self._guiComponent)

    def getTarget(self):
        return self._sceneRenderer.target


class MiniScreenTarget(MiniScreenBase):

    def __init__(self):
        MiniScreenBase.__init__(self, False)
        self.__targetLock = False
        self.onMiniScreenTargetInfoUpdate = Event()
        self.onMiniScreenTargetInfoVisibility = Event()
        self.onMiniScreenLockTargetVisibility = Event()
        self.updatePosition()

    def updatePosition(self):
        MiniScreenBase.updatePosition(self)

    def update(self):
        if self._isVisible() and self._sceneRenderer.target and not self._sceneRenderer.target.isDestroyed and self._sceneRenderer.target.inWorld:
            self.__updateTargetLockVisibility()
            self.onMiniScreenTargetInfoUpdate(self._sceneRenderer.target)

    def __updateTargetLockVisibility(self):
        isTargetLock = GameEnvironment.getHUD().isTargetLock() and self._guiComponent.visible
        if self.__targetLock != isTargetLock:
            self.__targetLock = isTargetLock
            self.onMiniScreenLockTargetVisibility(self.__targetLock)

    def setTarget(self, entity):
        if entity and self._isVisible():
            self._matrixProvider.target = entity.matrix
            self._sceneRenderer.target = entity
            self._sceneRenderer.targetCompound = entity.controllers['modelManipulator'].compoundIDProxy
            targetClassName = str(entity.__class__.__name__)
            if targetClassName in TEAM_OBJECT_CLASS_NAMES:
                self._matrixProvider.offset = HUD_MINISCREEN_OFFSET_BASE * WORLD_SCALING
            else:
                self._matrixProvider.offset = HUD_MINISCREEN_OFFSET_AIRPLANE * WORLD_SCALING
        else:
            self._sceneRenderer.target = None
            self._sceneRenderer.targetCompound = BigWorld.PyHandleProxy()
        self.setVisible(self._isVisible())
        self.__updateTargetLockVisibility()
        return

    def _initMatrixProvider(self):
        self._matrixProvider = BigWorld.CameraDirectionProvider()
        self._matrixProvider.offset = HUD_MINISCREEN_OFFSET_AIRPLANE * WORLD_SCALING
        self._matrixProvider.shiftUpDistance = HUD_MINISCREEN_OFFSET_ABOVE_GROUND

    def _getFov(self):
        return HUD_MINISCREEN_FOV

    def destroy(self):
        self._matrixProvider = BigWorld.CameraDirectionProvider()
        self.onMiniScreenTargetInfoVisibility(False)
        self.onMiniScreenTargetInfoUpdate.clear()
        self.onMiniScreenTargetInfoVisibility.clear()
        self.onMiniScreenLockTargetVisibility.clear()
        MiniScreenBase.destroy(self)

    def setVisible(self, flag):
        MiniScreenBase.setVisible(self, flag)
        self.onMiniScreenTargetInfoVisibility(self._guiComponent.visible)


class MiniScreenRearView(MiniScreenBase):

    def __init__(self):
        MiniScreenBase.__init__(self, True)
        self._sceneRenderer.target = BigWorld.player()
        self._sceneRenderer.targetCompound = 4294967295L

    def update(self):
        pass

    def setTarget(self, entity):
        pass

    def _initMatrixProvider(self):
        player = BigWorld.player()
        srcMtx = player.realMatrix
        offset = toVec4(self.__getCameraSettings().rearViewCamPos)
        target = toVec4(self.__getCameraSettings().rearViewCamDir)
        self._matrixProvider = BigWorld.RearViewMatrixProvider(srcMtx, offset, target)

    def _getFov(self):
        return self.__getCameraSettings().rearViewCamFov

    def __getCameraSettings(self):
        return db.DBLogic.g_instance.getAirplaneCameraPreset(BigWorld.player().settings.airplane.visualSettings.camera)