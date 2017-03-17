# Embedded file name: scripts/client/gui/HudElements/BombTarget.py
import BigWorld
import GUI
from ICMultiUpdate import ICMultiUpdate
import db.DBLogic
from consts import *
from gui.HUDconsts import *

class BombTarget(ICMultiUpdate):

    def __init__(self):
        self.__inited = False
        self.__visible = False
        ICMultiFunction = lambda : (self.__update() if self.__visible else None)
        ICMultiUpdate.__init__(self, (0.01666667, ICMultiFunction))
        self.__matrixProvider = None
        return

    def __update(self):
        self.__matrixProvider.dispersionAngle = BigWorld.player().controllers['shellController'].getBombDispersionAngle()

    def dispose(self):
        ICMultiUpdate.dispose(self)

    def restart(self):
        pass

    def __createTarget(self):
        self.__matrixProvider = GUI.BombTargetMp()
        self.__matrixProvider.target = BigWorld.player().realMatrix
        self.__matrixProvider.acceleration = db.DBLogic.g_instance.aircrafts.environmentConstants.gravityAcceleration.y * WORLD_SCALING
        self.__matrixProvider.worldScalingCfc = WORLD_SCALING
        self.__matrixProvider.speedScalingCfc = SPEED_SCALING
        self.__matrixProvider.minTargetSize = MIN_BOMB_TARGET_SIZE
        self.__matrixProvider.maxTargetSize = MAX_BOMB_TARGET_SIZE
        self.__matrixProvider.airResistance = AIR_RESISTANCE
        self.__matrixProvider.maxBombTrajectoryLength = MAX_FLIGHT_DISTANCE
        self.__matrixProvider.minBombFlightHeight = MIN_FLIGHT_HEIGHT
        self.__hud = GUI.BombSignHud()
        self.__hud.signModelName = BOMB_SIGN_VISUAL
        self.__hud.signDisabledModelName = BOMB_SIGN_DISABLED_VISUAL
        self.__hud.bombMP = self.__matrixProvider
        self.__hud.init()
        self.__signEnabled = True
        self.__inited = True
        self.__hud.visible = True
        GUI.addRoot(self.__hud)

    def setBombDispersionParams(self, dispaersionAngle):
        self.__matrixProvider.dispersionAngle = dispaersionAngle
        self.__matrixProvider.pitchSpeedCfc = BOMB_Z_SCATTER_SCALING

    def destroy(self):
        self.setVisible(False)
        if self.__inited:
            GUI.delRoot(self.__hud)
            self.__hud.bombMP = None
        self.__inited = False
        self.__visible = False
        self.__hud = None
        self.__cachedTexture = None
        self.dispose()
        return

    def setBombTargetEnable(self, signEnabled):
        if self.__signEnabled != signEnabled:
            if signEnabled:
                self.__hud.disabled = False
            else:
                self.__hud.disabled = True
            self.__signEnabled = signEnabled

    def getBombTargetEnable(self):
        return self.__signEnabled

    def setVisible(self, visible):
        if visible != self.__visible:
            self.__visible = visible
            if visible and not self.__inited:
                self.__createTarget()
            if self.__inited:
                self.__hud.visible = visible

    def isVisible(self):
        return self.__visible

    @property
    def matrixProvider(self):
        return self.__matrixProvider

    def disableUpdate(self, value):
        if self.__matrixProvider is not None:
            self.__matrixProvider.updateDisabled = value
        return