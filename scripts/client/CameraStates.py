# Embedded file name: scripts/client/CameraStates.py
import BigWorld
import GameEnvironment
import Math
import math
from MathExt import *
from consts import *
from StateMachine import *
import Settings
import collections
from debug_utils import *
from gui.HUDconsts import HUD_REDUCTION_POINT_SCALE
from clientConsts import CAMERA_ALT_MODE_SHIFT_VECTOR, CAMERA_ZOOM_PRESET
from EntityHelpers import isPlayerAvatar
from random import randint, uniform
g_useLowAltitudeCorrection = True

class ZSCameraData:

    def __init__(self, cameraToCursor, maxCursorSpeed, minCursorSpeed, cursorMaxSpeedAngle, cursorMinSpeedAngle, cursorUpToAircraft, cursorMaxRollSpeed, cursorMaxRollAcceleration, cursorBackSpeed):
        self.maxCursorSpeed = maxCursorSpeed
        self.minCursorSpeed = minCursorSpeed
        self.__cursorMinSpeedAngle = math.radians(cursorMinSpeedAngle)
        self.__cursorMaxSpeedAngle = math.radians(cursorMaxSpeedAngle)
        self.__cursorBackSpeed = math.radians(cursorBackSpeed)

    @property
    def cursorMinSpeedAngle(self):
        if self.__cursorMinSpeedAngle == 180.0:
            a = 1.0
        else:
            a = max(0.01, BigWorld.player().asymptoteVMaxPitch)
        return self.__cursorMinSpeedAngle * a

    @property
    def cursorMaxSpeedAngle(self):
        if self.__cursorMinSpeedAngle == 180.0:
            a = 1.0
        else:
            a = max(0.01, BigWorld.player().asymptoteVMaxPitch)
        return self.__cursorMaxSpeedAngle * a

    def setToStrategy(self, strategy):
        strategy.maxCursorSpeed = self.maxCursorSpeed
        strategy.minCursorSpeed = self.minCursorSpeed
        strategy.cursorMinSpeedAngle = self.cursorMinSpeedAngle
        strategy.cursorMaxSpeedAngle = self.cursorMaxSpeedAngle
        strategy.cursorBackSpeed = self.__cursorBackSpeed


class CameraState(object):
    NormalCombat = 0
    Free = 1
    Back = 2
    Left = 3
    Right = 4
    Top = 5
    Bottom = 6
    DestroyedFall = 7
    DestroyedLanded = 8
    Spectator = 9
    BottomLeft = 10
    BottomRight = 11
    TopLeft = 12
    TopRight = 13
    Bomb = 14
    Target = 15
    SuperFree = 16
    FreeFixable = 17
    TargetMe = 18
    NormalAssault = 19
    GamepadCombat = 22
    GamepadAssault = 23
    JoystickCombat = 24
    JoystickAssault = 25
    MouseCombat = 26
    MouseAssault = 27
    Empty = 28
    ReplayFree = 29
    SpectatorSide = 30
    DebugCamera = 31
    _context = None

    def __init__(self):
        self.returnToNormalTime = -1
        self.strategy = None
        return

    def enter(self, params = None):
        pass

    def exit(self):
        self.strategy = None
        return

    def reEnter(self, params = None):
        pass

    def updateParams(self, params = None):
        pass

    def getReturnToNormalTime(self):
        return -1.0

    def refreshState(self):
        pass

    @staticmethod
    def setInitParams(stateInitParams):
        CameraState._context = stateInitParams

    def zoomPresent(self):
        return False

    def onZoomIndexChanged(self, zoomIndex, zoomData):
        pass

    def getZoomDataPosition(self, zoomData):
        return zoomData.position


class CameraStateMachine(StateMachine):

    def __init__(self):
        StateMachine.__init__(self)
        self.__stateStack = collections.deque()
        self.__cachedStateParams = {}
        self.__modalStates = set([CameraState.SpectatorSide])

    COMPOSITE_STATES = {(CameraState.Top, CameraState.Right): CameraState.TopRight,
     (CameraState.Top, CameraState.Left): CameraState.TopLeft,
     (CameraState.Bottom, CameraState.Right): CameraState.BottomRight,
     (CameraState.Bottom, CameraState.Left): CameraState.BottomLeft}

    def __compositeLastStates(self):
        stackSize = len(self.__stateStack)
        if stackSize > 1:
            if (self.__stateStack[-1], self.__stateStack[-2]) in CameraStateMachine.COMPOSITE_STATES:
                return CameraStateMachine.COMPOSITE_STATES[self.__stateStack[-1], self.__stateStack[-2]]
            if (self.__stateStack[-2], self.__stateStack[-1]) in CameraStateMachine.COMPOSITE_STATES:
                return CameraStateMachine.COMPOSITE_STATES[self.__stateStack[-2], self.__stateStack[-1]]
        if stackSize == 0:
            LOG_WARNING('CameraStateMachine: state stack is empty!')
            return CameraState.NormalCombat
        else:
            return self.__stateStack[-1]

    def setState(self, name, params = None, addToStack = True):
        curState = self.getState()
        if name != curState:
            if addToStack and name not in self.__stateStack:
                self.__stateStack.append(name)
                if params:
                    self.__cachedStateParams[name] = params
            if curState in self.__modalStates and curState in self.__stateStack:
                self.setPrevState(name)
            else:
                newState = self.__compositeLastStates()
                returnToNormalTime = -1
                if self.currentState:
                    returnToNormalTime = self.currentState.getReturnToNormalTime()
                self.getStateObject(newState).returnToNormalTime = returnToNormalTime
                StateMachine.setState(self, newState, params)
        elif curState not in self.__modalStates:
            self._reEnterState(params)

    def setPrevState(self, newState):
        temp = self.__stateStack.pop()
        if temp != newState:
            self.__stateStack.append(newState)
        self.__stateStack.append(temp)

    def leaveState(self, name = None):
        if len(self.__stateStack) > 1:
            newState = None
            if name is None:
                self.__stateStack.pop()
                newState = self.__stateStack[-1]
            elif name in self.__stateStack:
                self.__stateStack.remove(name)
                newState = self.__stateStack[-1]
            if newState is not None:
                params = self.__cachedStateParams[newState] if newState in self.__cachedStateParams else None
                self.setState(newState, params, False)
        return

    def destroy(self):
        self.getCurStateObject().exit()

    def reset(self):
        StateMachine.reset(self)
        self.__stateStack.clear()
        self.__cachedStateParams.clear()

    def getPrevState(self):
        if len(self.__stateStack) >= 2:
            return self.__stateStack[-2]
        else:
            return None
            return None


class BattleCameraStateMachine(CameraStateMachine):

    def __init__(self):
        CameraStateMachine.__init__(self)
        self.addState(CameraState.Empty, CameraStateEmpty())
        self.addState(CameraState.NormalCombat, CameraStateNormalCombat())
        self.addState(CameraState.NormalAssault, CameraStateNormalAssault())
        self.addState(CameraState.MouseCombat, CameraStateMouseCombat())
        self.addState(CameraState.MouseAssault, CameraStateMouseAssault())
        self.addState(CameraState.GamepadCombat, CameraStateGamepadCombat())
        self.addState(CameraState.GamepadAssault, CameraStateGamepadAssault())
        self.addState(CameraState.JoystickCombat, CameraStateJoystickCombat())
        self.addState(CameraState.JoystickAssault, CameraStateJoystickAssault())
        self.addState(CameraState.Free, CameraStateFree())
        self.addState(CameraState.Back, CameraStateBack())
        self.addState(CameraState.Left, CameraStateSideLeft())
        self.addState(CameraState.Right, CameraStateSideRight())
        self.addState(CameraState.Top, CameraStateSideTop())
        self.addState(CameraState.Bottom, CameraStateSideBottom())
        self.addState(CameraState.Spectator, CameraStateSpectator())
        self.addState(CameraState.BottomLeft, CameraStateSideBottomLeft())
        self.addState(CameraState.BottomRight, CameraStateSideBottomRight())
        self.addState(CameraState.TopLeft, CameraStateSideTopLeft())
        self.addState(CameraState.TopRight, CameraStateSideTopRight())
        self.addState(CameraState.Target, CameraStateTarget())
        self.addState(CameraState.SuperFree, CameraStateSuperFree())
        self.addState(CameraState.FreeFixable, CameraStateFreeFixable())
        self.addState(CameraState.DestroyedFall, CameraStateDestroyedFall())
        self.addState(CameraState.DestroyedLanded, CameraStateDestroyedLanded())
        self.addState(CameraState.TargetMe, CameraStateTargetOnMe())
        self.addState(CameraState.ReplayFree, CameraStateFree())
        self.addState(CameraState.SpectatorSide, CameraStateSpectatorSide())
        self.addState(CameraState.DebugCamera, CameraStateDebugCamera())
        self.setState(CameraState.Empty)

    def reset(self):
        CameraStateMachine.reset(self)
        self.setState(CameraState.Empty)


def _dCursorToTarget(targetVec3):
    direction = BigWorld.camera().position - targetVec3
    BigWorld.dcursor().pitch = -direction.pitch
    BigWorld.dcursor().yaw = direction.yaw
    BigWorld.dcursor().roll = 0.0


class CameraStateEmpty(CameraState):
    pass


class CameraStateWithZoom(CameraState):

    def __init__(self):
        CameraState.__init__(self)
        self.__timerIn = 0.0
        self.__timerOut = 0.0
        self.__height = 1.0
        self.strategy = None
        return

    def _createStrategy(self):
        pass

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.DEFAULT

    def zoomPresent(self):
        return True

    def enter(self, params = None):
        if self.strategy is None:
            self._createStrategy()
        self.__centralHudToCam = False
        zoomIndex = self._context.getDestZoomDataIdx()
        self._context.setZoom(zoomIndex, self.zoomPreset())
        GameEnvironment.getHUD().setTargetVisible(True)
        self._context.cameraInstance.setStrategy(self.strategy, self._getInterpolationTime())
        self._checkCenterHudMatrix()
        import CameraEffect
        if CameraEffect.g_instance:
            CameraEffect.g_instance.startAccelerationEffect()
        return

    def onZoomIndexChanged(self, zoomIndex, zoomData):
        self._checkCenterHudMatrix()

    def _checkCenterHudMatrix(self):
        self.__setCenterHudMatrix(True)

    def _getCenterHudMatrix(self):
        return None

    def __setCenterHudMatrix(self, active):
        if active != self.__centralHudToCam:
            import BattleReplay
            self.__centralHudToCam = active
            if active:
                GameEnvironment.getHUD().restoreEntityesHudCursorMatrixProvider()
                centerHudMatrix = self._getCenterHudMatrix()
                if centerHudMatrix is not None:
                    if BattleReplay.isPlaying():
                        GameEnvironment.getHUD().centerPoint().setMatrixProvider(BattleReplay.g_replay.getCenterPointMatrixProvider())
                    else:
                        GameEnvironment.getHUD().centerPoint().setMatrixProvider(centerHudMatrix)
                    BattleReplay.g_replay.notifyNewCPMatrix(centerHudMatrix)
            else:
                GameEnvironment.getHUD().centerPoint().removeMatrixProvider()
                GameEnvironment.getHUD().removeEntityesHudCursorMatrixProvider()
                BattleReplay.g_replay.notifyNewCPMatrix(None)
        return

    def exit(self):
        GameEnvironment.getHUD().setTargetVisible(False)
        self.__setCenterHudMatrix(False)

    def getZoomDataPositionLinier(self, zoomData):
        if g_useLowAltitudeCorrection and self._context.entity.id == BigWorld.player().id:
            switchTime = lambda maxValue: maxValue * (1.0 - 0.5 * self._context.entity.speed / VELLOCITY_OF_SOUND)
            height = self._context.entity.altitudeAboveObstacle
            if self.__timerIn > BigWorld.time():
                self.__height = clamp(CAM_BOTTOM_POSITION, self.__height + CAM_FALL_SPEED, 1)
                if height > CRITICAL_HEIGHT_ENABLE:
                    self.__timerIn = BigWorld.time() + switchTime(SWITCH_ALTITUDE_TIME_IN)
                return Math.Vector3(zoomData.position.x, self.__height * zoomData.position.y, zoomData.position.z)
            if height < CRITICAL_HEIGHT_ENABLE:
                self.__height = clamp(CAM_BOTTOM_POSITION, self.__height - CAM_FALL_SPEED, 1)
                self.__timerOut = BigWorld.time() + switchTime(SWITCH_ALTITUDE_TIME_OUT)
                return Math.Vector3(zoomData.position.x, self.__height * zoomData.position.y, zoomData.position.z)
            if self.__timerOut > BigWorld.time():
                return Math.Vector3(zoomData.position.x, self.__height * zoomData.position.y, zoomData.position.z)
            self.__timerIn = BigWorld.time() + SWITCH_ALTITUDE_TIME_IN
        return Math.Vector3(zoomData.position.x, self.__height * zoomData.position.y, zoomData.position.z)

    def _getInterpolationTime(self):
        interpolationTime = self._context.cameraSettings.normalCamInterpolationTime
        if self.returnToNormalTime != -1:
            interpolationTime = self.returnToNormalTime
        return interpolationTime


class CameraStateNormalBase(CameraStateWithZoom):

    def _createStrategy(self):
        self.strategy = self._context.defaultStrategies['CameraStrategyNormal']

    def enter(self, params = None):
        CameraStateWithZoom.enter(self, params)
        self._context.cameraManager.eSetCameraRingVisible(False)

    def _getCenterHudMatrix(self):
        offsetMatrix = Math.Matrix()
        offsetMatrix.translation = self._context.reductionPoint * HUD_REDUCTION_POINT_SCALE
        matr = Math.MatrixProduct()
        matr.a = offsetMatrix
        matr.b = self._context.entity.realMatrix
        return matr

    def refreshState(self):
        self._context.cameraInstance.setStrategy(self.strategy, 0.0)


class CameraStateDebugCamera(CameraStateNormalBase):

    def _createStrategy(self):
        self.strategy = self._context.defaultStrategies['CameraStrategyNormal']

    def enter(self, params = None):
        CameraStateNormalBase.enter(self, params)
        self.strategy.sourceMatrix = BigWorld.player().realMatrix

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.NORMAL_COMBAT

    def getZoomDataPosition(self, zoomData):
        return self.getZoomDataPositionLinier(zoomData)


class CameraStateNormalCombat(CameraStateNormalBase):

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.NORMAL_COMBAT

    def getZoomDataPosition(self, zoomData):
        return self.getZoomDataPositionLinier(zoomData)

    def enter(self, params = None):
        CameraStateNormalBase.enter(self, params)
        self._context.applyZoomStateFov(self._getInterpolationTime(), True)


class CameraStateNormalAssault(CameraStateNormalBase):

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.NORMAL_ASSAULT

    def enter(self, params = None):
        CameraStateNormalBase.enter(self, params)
        self._context.applyZoomStateFov(self._getInterpolationTime())


class CameraStateJoystickCombat(CameraStateNormalBase):

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.JOYSTICK_COMBAT

    def getZoomDataPosition(self, zoomData):
        return self.getZoomDataPositionLinier(zoomData)

    def enter(self, params = None):
        CameraStateNormalBase.enter(self, params)
        self._context.applyZoomStateFov(self._getInterpolationTime(), True)


class CameraStateJoystickAssault(CameraStateNormalBase):

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.JOYSTICK_ASSAULT

    def enter(self, params = None):
        CameraStateNormalBase.enter(self, params)
        self._context.applyZoomStateFov(self._getInterpolationTime())


class CameraStateMouseBase(CameraStateWithZoom):

    def __init__(self):
        CameraStateWithZoom.__init__(self)
        self.onZoomTableChanged(1.0)

    def enter(self, params = None):
        CameraStateWithZoom.enter(self, params)
        self.strategy.bottomPitchBound = math.radians(90.0)
        self.strategy.topPitchBound = math.radians(90.0)
        self._context.cameraManager.eSetCameraRingVisible(True)
        self.onZoomIndexChanged(self._context.getDestZoomDataIdx(), None)
        return

    def _createStrategy(self):
        self.strategy = self._context.defaultStrategies['CameraStrategyMouse']

    def _getCenterHudMatrix(self):
        offsetMatrix = Math.Matrix()
        offsetMatrix.translation = self._context.reductionPoint * HUD_REDUCTION_POINT_SCALE
        matr = Math.MatrixProduct()
        matr.a = offsetMatrix
        matr.b = self.strategy.cursorMatrixProvider
        return matr

    def onZoomIndexChanged(self, zoomIndex, zoomData):
        CameraStateWithZoom.onZoomIndexChanged(self, zoomIndex, zoomData)
        self.__zSCameraTable[zoomIndex].setToStrategy(self.strategy)

    def onZoomTableChanged(self, cameraToCursor):
        self.__zSCameraTable = [ZSCameraData(cameraToCursor, 180.0, 180.0, 180.0, 181.0, 0.1, 120.0, 30.0, 0.0),
         ZSCameraData(cameraToCursor, 90.0, 90.0, 180.0, 181.0, 0.15, 120.0, 30.0, 0.0),
         ZSCameraData(cameraToCursor, 70.0, 30.0, 90.0, 180.0, 0.2, 120.0, 30.0, 0.0),
         ZSCameraData(cameraToCursor, 50.0, 5.0, 0.0, 60.0, 0.25, 120.0, 30.0, 100),
         ZSCameraData(cameraToCursor, 25.0, 5.0, 0.0, 30.0, 0.3, 120.0, 30.0, 50)]


class CameraStateMouseCombat(CameraStateMouseBase):

    def enter(self, params = None):
        CameraStateMouseBase.enter(self, params)
        self.strategy.bottomPitchBound = math.radians(90.0)
        self.strategy.topPitchBound = math.radians(90.0)

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.DIRECT_COMBAT

    def getZoomDataPosition(self, zoomData):
        return self.getZoomDataPositionLinier(zoomData)

    def enter(self, params = None):
        CameraStateMouseBase.enter(self, params)
        self._context.applyZoomStateFov(self._getInterpolationTime(), True)


class CameraStateMouseAssault(CameraStateMouseBase):

    def enter(self, params = None):
        CameraStateMouseBase.enter(self, params)
        self.strategy.bottomPitchBound = math.radians(45.0)
        self.strategy.topPitchBound = math.radians(45.0)

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.DIRECT_ASSAULT

    def enter(self, params = None):
        CameraStateMouseBase.enter(self, params)
        self._context.applyZoomStateFov(self._getInterpolationTime())


class CameraStateGamepadCombat(CameraStateMouseBase):

    def _createStrategy(self):
        self.strategy = self._context.defaultStrategies['CameraStrategyGamepad']


class CameraStateGamepadAssault(CameraStateMouseBase):

    def enter(self, params = None):
        CameraStateMouseBase.enter(self, params)
        self.onZoomIndexChanged(0, None)
        self.strategy.bottomPitchBound = math.radians(45.0)
        self.strategy.topPitchBound = math.radians(45.0)
        return

    def _createStrategy(self):
        self.strategy = self._context.defaultStrategies['CameraStrategyGamepad']

    def zoomPreset(self):
        return CAMERA_ZOOM_PRESET.DIRECT_ASSAULT


class CameraStateFree(CameraState):

    def __init__(self):
        CameraState.__init__(self)
        self.__invertVertical = False
        self._pivotDist = None
        return

    def _initPivotDist(self):
        self._pivotDist = (self._context.cameraSettings.pivotDistMin, self._context.cameraSettings.pivotDistMax)

    def onMouseScroll(self, dz):
        if dz and self.strategy:
            newDist = self.strategy.distance - dz * self._context.cameraSettings.freeCamZoomFactor
            self.strategy.distance = newDist
            self.setFovByDistance(newDist, self._context.cameraSettings.freeCamFovInterpolationTime)
            return newDist

    def setFovByDistance(self, distance, rampTime):
        distMin = self._pivotDist[0]
        distMax = self._pivotDist[1]
        distance = clamp(distMin, distance, distMax)
        k = (distance - distMin) / (distMax - distMin)
        newFov = (self._context.cameraManager.getMaxMouseCombatFov() - self._context.cameraSettings.minMouseCombatFov) * k + self._context.cameraSettings.minMouseCombatFov
        BigWorld.projection().rampFov(math.radians(self._context.cameraManager.convertToVerticalFOV(newFov)), rampTime)

    def setInvertVertical(self, value):
        LOG_DEBUG('setInvertVertical %s' % value)
        BigWorld.dcursor().invertVerticalMovement = bool(value)

    def __startInterpolation(self, duration):
        self.__sensitivity = BigWorld.dcursor().mouseSensitivity
        BigWorld.dcursor().mouseSensitivity = self.__sensitivity * 0.2

    def __endInterpolation(self):
        BigWorld.dcursor().mouseSensitivity = self.__sensitivity

    def enter(self, params = None):
        import BattleReplay
        self._context.setModelVisible(True)
        if not self._context.cameraManager.isSniperMode:
            _dCursorToTarget(Math.Matrix(self._context.mainMatrixProvider).translation)
        else:
            direction = -Math.Matrix(self._context.entity.realMatrix).applyToAxis(2)
            BigWorld.dcursor().pitch = -direction.pitch
            BigWorld.dcursor().yaw = direction.yaw
            BigWorld.dcursor().roll = 0.0
        self._initPivotDist()
        self.__invertVertical = BigWorld.dcursor().invertVerticalMovement
        pivotDistMin, pivotDistMax = self._pivotDist[0], self._pivotDist[1]
        distance = self._context.getCurZoomlessOffset().length
        self.strategy = BigWorld.CameraStrategyFree(distance, BigWorld.dcursor().matrix, pivotDistMin, pivotDistMax, self._context.mainMatrixProvider)
        self.strategy.interpolationEndCallback = self.__endInterpolation
        self.strategy.interpolationStartCallback = self.__startInterpolation
        self.strategy.aroundLocalAxes = bool(Settings.g_instance.cinemaCamera)
        self.strategy.invertVertical = bool(self.__invertVertical)
        self.setFovByDistance(distance, self._context.cameraSettings.freeCamInterpolationTime)
        self._context.cameraInstance.setStrategy(self.strategy, self._context.cameraSettings.freeCamInterpolationTime if not BattleReplay.isPlaying() else 0, True)
        self.strategy.distanceHalflife = self._context.cameraSettings.freeCamDistHalflife
        player = BigWorld.player()
        GameEnvironment.getCamera().setCameraOffset(player.settings.airplane.visualSettings.cameraOffset - player.settings.hpmass.mass.position)
        self.strategy.pitchClampingEnabled = True

    def exit(self):
        GameEnvironment.getCamera().setCameraOffset(Math.Vector3(0.0, 0.0, 0.0))
        self.strategy.pitchClampingEnabled = False
        self.setInvertVertical(self.__invertVertical)

    def getReturnToNormalTime(self):
        if not Settings.g_instance.cinemaCamera:
            return 0.0
        else:
            return -1.0


class CameraStateSuperFree(CameraState):

    def onMouseScroll(self, dz):
        if dz and self.strategy:
            self.strategy.distance -= dz * 0.01

    @property
    def distance(self):
        return self.strategy.distance

    def enter(self, params = None):
        self._context.setModelVisible(True)
        _dCursorToTarget(Math.Matrix(self._context.mainMatrixProvider).translation)
        self.strategy = BigWorld.CameraStrategySuperFree(BigWorld.dcursor().matrix)
        self._context.cameraInstance.setStrategy(self.strategy, 0.0)

    def exit(self):
        CameraState.exit(self)


class CameraStateBack(CameraState):

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        self._context.setModelVisible(True)
        reductionPt = self._context.reductionPoint * HUD_REDUCTION_POINT_SCALE
        self.strategy = BigWorld.CameraStrategyFixed(cameraSettings.backCamPos, -reductionPt, Math.Vector3(0.0, 1.0, 0.0), self._context.mainMatrixProvider)
        BigWorld.projection().rampFov(math.radians(cameraSettings.backCamFov), cameraSettings.backCamInterpolationTime)
        self._context.cameraInstance.setStrategy(self.strategy, cameraSettings.backCamInterpolationTime, True)

    def getReturnToNormalTime(self):
        return 0.0


class CameraStateSide(CameraState):

    def __init__(self):
        CameraState.__init__(self)

    def _setTransformation(self, pos, direction, dirUp):
        self.__pos = pos
        self.__dir = direction
        self.__dirUp = dirUp

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        sideShift = CAMERA_ALT_MODE_SHIFT_VECTOR if self._context.isAltMode() else Math.Vector3(0.0, 0.0, 0.0)
        self.strategy = BigWorld.CameraStrategyFixed(self.__pos, self.__dir + sideShift, self.__dirUp, self._context.mainMatrixProvider)
        BigWorld.projection().rampFov(self._context.normalFov, cameraSettings.sideCamInterpolationTime)
        self._context.cameraInstance.setStrategy(self.strategy, cameraSettings.sideCamInterpolationTime, True)

    def reEnter(self, params = None):
        self.enter(params)


class CameraStateSideLeft(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        self._setTransformation(self._context.cameraSettings.leftCamPos, self._context.cameraSettings.leftCamDir, Math.Vector3(0.0, 1.0, 0.0))
        CameraStateSide.enter(self, params)


class CameraStateSideRight(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        self._setTransformation(self._context.cameraSettings.rightCamPos, self._context.cameraSettings.rightCamDir, Math.Vector3(0.0, 1.0, 0.0))
        CameraStateSide.enter(self, params)


class CameraStateSideTop(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        self._setTransformation(self._context.cameraSettings.topCamPos, self._context.cameraSettings.topCamDir, Math.Vector3(0.0, 0.0, -1.0))
        CameraStateSide.enter(self, params)


class CameraStateSideBottom(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        self._setTransformation(self._context.cameraSettings.bottomCamPos, self._context.cameraSettings.bottomCamDir, Math.Vector3(0.0, 0.0, 1.0))
        CameraStateSide.enter(self, params)


class CameraStateSideBottomLeft(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        rotMatrix = Math.Matrix()
        rotMatrix.setRotateY(math.radians(-45))
        pos = rotMatrix.applyVector(self._context.cameraSettings.leftCamPos)
        direction = rotMatrix.applyVector(self._context.cameraSettings.leftCamDir)
        self._setTransformation(pos, direction, Math.Vector3(0.0, 1.0, 0.0))
        CameraStateSide.enter(self, params)


class CameraStateSideBottomRight(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        rotMatrix = Math.Matrix()
        rotMatrix.setRotateY(math.radians(45))
        pos = rotMatrix.applyVector(self._context.cameraSettings.rightCamPos)
        direction = rotMatrix.applyVector(self._context.cameraSettings.rightCamDir)
        self._setTransformation(pos, direction, Math.Vector3(0.0, 1.0, 0.0))
        CameraStateSide.enter(self, params)


class CameraStateSideTopLeft(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        rotMatrix = Math.Matrix()
        rotMatrix.setRotateY(math.radians(45))
        pos = rotMatrix.applyVector(self._context.cameraSettings.leftCamPos)
        direction = rotMatrix.applyVector(self._context.cameraSettings.leftCamDir)
        self._setTransformation(pos, direction, Math.Vector3(0.0, 1.0, 0.0))
        CameraStateSide.enter(self, params)


class CameraStateSideTopRight(CameraStateSide):

    def __init__(self):
        CameraStateSide.__init__(self)

    def enter(self, params = None):
        rotMatrix = Math.Matrix()
        rotMatrix.setRotateY(math.radians(-45))
        pos = rotMatrix.applyVector(self._context.cameraSettings.rightCamPos)
        direction = rotMatrix.applyVector(self._context.cameraSettings.rightCamDir)
        self._setTransformation(pos, direction, Math.Vector3(0.0, 1.0, 0.0))
        CameraStateSide.enter(self, params)


class CameraStateDestroyedFall(CameraState):
    TERRAIN_COLLISION_TRACE_INTERVAL = 0.5

    def __init__(self):
        CameraState.__init__(self)
        self.__cbAnimationDelay = None
        self.__cbGroundCam = None
        self.prevStrategy = None
        return

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        cameraInstance = self._context.cameraInstance
        destroyedFallSettings = cameraSettings.destroyedFall
        self._context.setModelVisible(True)
        BigWorld.projection().rampFov(destroyedFallSettings.animationFov, destroyedFallSettings.stateInterpolationTime)
        _dCursorToTarget(Math.Matrix(self._context.mainMatrixProvider).translation)
        self.strategy = BigWorld.CameraStrategyDestroyedFall(self._context.getCurZoomlessOffset().length, BigWorld.dcursor().matrix, cameraSettings.pivotDistMin, cameraSettings.pivotDistMax, self._context.mainMatrixProvider)
        self.strategy.aroundLocalAxes = False
        cameraInstance.setStrategy(self.strategy, destroyedFallSettings.stateInterpolationTime)
        self.__checkAnimation()

    def exit(self):
        CameraState.exit(self)
        self.__clearCallbacks()
        BigWorld.dcursor().mouseLocked = False
        cameraInstance = self._context.cameraInstance
        cameraInstance.parentMatrix = self._context.mainMatrixProvider
        BigWorld.dcursor().stopPitchAnimation()
        BigWorld.dcursor().stopYawAnimation()

    def __clearCallbacks(self):
        if self.__cbAnimationDelay:
            BigWorld.cancelCallback(self.__cbAnimationDelay)
            self.__cbAnimationDelay = None
        if self.__cbGroundCam:
            BigWorld.cancelCallback(self.__cbGroundCam)
            self.__cbGroundCam = None
        return

    def __checkAnimation(self):
        cameraSettings = self._context.cameraSettings
        destroyedFallSettings = cameraSettings.destroyedFall
        curPlayerMatrix = Math.Matrix(self._context.mainMatrixProvider)
        airplaneDir = curPlayerMatrix.applyToAxis(2)
        animationReadyDistance = self._context.entity.getSpeed() * destroyedFallSettings.animationNeedTime
        collideData = BigWorld.hm_collideSimple(self._context.entity.spaceID, curPlayerMatrix.translation, curPlayerMatrix.translation + airplaneDir * animationReadyDistance)
        if not collideData:
            self.__cbAnimationDelay = BigWorld.callback(destroyedFallSettings.animationStartTime, self.__startAnimation)
            BigWorld.dcursor().mouseLocked = True

    def __startAnimation(self):
        cameraSettings = self._context.cameraSettings
        destroyedFallSettings = cameraSettings.destroyedFall
        self.strategy.distanceAnimationTime = destroyedFallSettings.animationTime
        self.strategy.distanceAnimationFadeInTime = destroyedFallSettings.animationFadeInTime
        self.strategy.distanceAnimationFadeOutTime = destroyedFallSettings.animationFadeOutTime
        self.strategy.distance = destroyedFallSettings.animationDistance
        dPitch = destroyedFallSettings.animationPitch - BigWorld.dcursor().pitch
        pitchClockwise = dPitch > 0.0 if abs(dPitch) < math.pi else dPitch < 0.0
        BigWorld.dcursor().startPitchAnimation(destroyedFallSettings.animationPitch, destroyedFallSettings.animationTime, destroyedFallSettings.animationFadeInTime, destroyedFallSettings.animationFadeOutTime, pitchClockwise)
        BigWorld.dcursor().startYawAnimation(destroyedFallSettings.animationYaw, destroyedFallSettings.animationTime, destroyedFallSettings.animationFadeInTime, destroyedFallSettings.animationFadeOutTime, destroyedFallSettings.animationYawClockwise)
        if destroyedFallSettings.animationGroundTime > 0.0:
            self.__cbGroundCam = BigWorld.callback(destroyedFallSettings.animationTime, self.__checkGroundCam)

    def __checkGroundCam(self):
        cameraSettings = self._context.cameraSettings
        destroyedFallSettings = cameraSettings.destroyedFall
        curPlayerMatrix = Math.Matrix(self._context.mainMatrixProvider)
        airplaneDir = self._context.entity.getWorldVector()
        airplaneDir.normalise()
        animationReadyDistance = self._context.entity.getSpeed() * destroyedFallSettings.animationGroundNeedTime * WORLD_SCALING
        collideData = BigWorld.hm_collideSimple(self._context.entity.spaceID, curPlayerMatrix.translation, curPlayerMatrix.translation + airplaneDir * 99999.9)
        if collideData:
            collidePoint = collideData[0]
            distanceToGroundSquared = (collidePoint - curPlayerMatrix.translation).lengthSquared
            if animationReadyDistance * animationReadyDistance < distanceToGroundSquared:
                xShift = uniform(-destroyedFallSettings.animationGroundSpawnRadius, destroyedFallSettings.animationGroundSpawnRadius)
                yShift = uniform(-destroyedFallSettings.animationGroundSpawnRadius, destroyedFallSettings.animationGroundSpawnRadius)
                cameraPos = collidePoint + Math.Vector3(xShift, yShift, 0.0)
                newDir = (cameraPos - curPlayerMatrix.translation).getNormalized()
                collideData = BigWorld.hm_collideSimple(self._context.entity.spaceID, curPlayerMatrix.translation, curPlayerMatrix.translation + newDir * 99999.9)
                if collideData:
                    collidePoint = collideData[0]
                    collidePoint.y += destroyedFallSettings.animationGroundHeight
                    srcMatrixProvider = Math.Matrix()
                    srcMatrixProvider.setTranslate(collidePoint)
                    self.prevStrategy = self.strategy
                    self.strategy = BigWorld.CameraStrategyTarget(srcMatrixProvider, Math.Vector3(0, 0, 0), self._context.mainMatrixProvider)
                    cameraInstance = self._context.cameraInstance
                    cameraInstance.setStrategy(self.strategy, 0.0)
                    cameraInstance.parentMatrix = srcMatrixProvider
                    BigWorld.projection().rampFov(destroyedFallSettings.animationGroundFov, 0.0)
                    self.__cbGroundCam = BigWorld.callback(destroyedFallSettings.animationGroundTime, self.__exitGroundCam)

    def __exitGroundCam(self):
        cameraSettings = self._context.cameraSettings
        destroyedFallSettings = cameraSettings.destroyedFall
        cameraInstance = self._context.cameraInstance
        self.strategy = self.prevStrategy
        cameraInstance.setStrategy(self.strategy, 0.0)
        cameraInstance.parentMatrix = self._context.mainMatrixProvider
        BigWorld.projection().rampFov(destroyedFallSettings.animationFov, 0.0)

    def reEnter(self, params = None):
        self.__clearCallbacks()
        self.enter(params)


class CameraStateDestroyedLanded(CameraState):

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        cameraInstance = self._context.cameraInstance
        destroyedLandedSettings = cameraSettings.destroyedLanded
        self._context.setModelVisible(True)
        self.__prevParentMatrix = cameraInstance.parentMatrix
        cameraInstance.parentMatrix = Math.Matrix(cameraInstance.parentMatrix)
        correctPosTracerStart = Math.Vector3(cameraInstance.parentMatrix.translation)
        correctPosTracerStart.y += 2.0
        collideData = BigWorld.hm_collideSimple(self._context.entity.spaceID, correctPosTracerStart, cameraInstance.parentMatrix.translation)
        if collideData:
            cameraInstance.parentMatrix.translation = collideData[0]
        half_PI = math.pi * 0.5
        if destroyedLandedSettings.pitch < half_PI:
            conePos = cameraInstance.parentMatrix.translation
            coneAngle = half_PI - destroyedLandedSettings.pitch
            coneHeight = destroyedLandedSettings.distance * math.sin(destroyedLandedSettings.pitch)
            isConeCollided = BigWorld.hm_collideCone(self._context.entity.spaceID, conePos, coneAngle, coneHeight)
            if not isConeCollided:
                self.strategy = BigWorld.CameraStrategyFree(destroyedLandedSettings.distance, BigWorld.dcursor().matrix, destroyedLandedSettings.distance, destroyedLandedSettings.distance, cameraInstance.parentMatrix)
                self.strategy.aroundLocalAxes = False
                cameraInstance.setStrategy(self.strategy, destroyedLandedSettings.stateInterpolationTime)
                BigWorld.dcursor().yawSpeed = destroyedLandedSettings.rotationSpeed * randint(0, 1)
                BigWorld.dcursor().mouseLocked = True
                BigWorld.dcursor().pitch = destroyedLandedSettings.pitch
                BigWorld.dcursor().yaw = destroyedLandedSettings.yaw
        else:
            LOG_ERROR('destroyedLandedSettings.pitch is greater or equal 90 degrees!')

    def getReturnToNormalTime(self):
        return 0.0

    def exit(self):
        CameraState.exit(self)
        self._context.cameraInstance.parentMatrix = self.__prevParentMatrix
        BigWorld.dcursor().mouseLocked = False
        BigWorld.dcursor().yawSpeed = 0.0


class CameraStateSpectator(CameraStateFree):

    def __init__(self):
        CameraStateFree.__init__(self)
        self.__cameraTarget = None
        self.__lastRelDistance = None
        return

    def _initPivotDist(self):
        cameraSettings = self._context.cameraSettings
        zoomData = cameraSettings.zoomTable[Settings.g_instance.cameraZoomType][self._getZoomPresetPivotDist()]
        self._pivotDist = (abs(zoomData[len(zoomData) - 2].position.z), abs(zoomData[0].position.z))

    def onMouseScroll(self, dz):
        newDist = CameraStateFree.onMouseScroll(self, dz)
        if newDist is not None:
            self.__calcRelDistance(newDist)
            return newDist
        else:
            return

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        cameraInstance = self._context.cameraInstance
        self._initPivotDist()
        BigWorld.dcursor().pitch = 0
        BigWorld.dcursor().yaw = 0
        if self.__lastRelDistance is None:
            self.__calcRelDistance(self._context.getCurZoomlessOffset().length)
        pivotDistMin, pivotDistMax = self._pivotDist[0], self._pivotDist[1]
        distanceRange = pivotDistMax - pivotDistMin
        absDistance = pivotDistMin + self.__lastRelDistance * distanceRange
        self.strategy = BigWorld.CameraStrategyFree(absDistance, BigWorld.dcursor().matrix, pivotDistMin, pivotDistMax, self._context.mainMatrixProvider)
        self.strategy.aroundLocalAxes = False
        self.strategy.distanceHalflife = self._context.cameraSettings.freeCamDistHalflife
        cameraInstance.setStrategy(self.strategy, cameraSettings.spectatorCamInterpolationTime)
        self.setFovByDistance(absDistance, cameraSettings.spectatorCamInterpolationTime)
        self.strategy.pitchClampingEnabled = True
        return

    def reEnter(self, params = None):
        self.enter(params)

    def __calcRelDistance(self, absDistance):
        pivotDistMin, pivotDistMax = self._pivotDist[0], self._pivotDist[1]
        checkedDist = clamp(pivotDistMin, absDistance, pivotDistMax)
        distanceRange = pivotDistMax - pivotDistMin
        self.__lastRelDistance = (checkedDist - pivotDistMin) / distanceRange

    def getReturnToNormalTime(self):
        return -1.0

    def _getZoomPresetPivotDist(self):
        return CAMERA_ZOOM_PRESET.DIRECT_COMBAT

    def updateTarget(self):
        if self.strategy:
            self._initPivotDist()
            self.strategy.distanceMin = self._pivotDist[0]
            self.strategy.distanceMax = self._pivotDist[1]
            self.strategy.distance = self.strategy.distance
            self.strategy.sourceProvider = self._context.mainMatrixProvider
        else:
            LOG_ERROR("Cannot update the target because the strategy isn't exist!")


class CameraStateTarget(CameraState):

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        cameraInstance = self._context.cameraInstance
        self._context.setModelVisible(True)
        self.strategy = BigWorld.CameraStrategyTarget(self._context.mainMatrixProvider, self._context.getCurZoomlessOffset(), self._context.targetMatrix)
        self.strategy.worldUp = False
        BigWorld.projection().rampFov(self._context.normalFov, cameraSettings.targetCamInterpolationTime)
        cameraInstance.setStrategy(self.strategy, cameraSettings.targetCamInterpolationTime)

    def reEnter(self, params = None):
        self.enter(params)


class CameraStateTargetOnMe(CameraStateTarget):
    pass


class CameraStateFreeFixable(CameraState):
    PITCH_MIN = -math.pi * 0.5 + 0.3
    PITCH_MAX = math.pi * 0.5 - 0.3

    def enter(self, params = None):
        cameraSettings = self._context.cameraSettings
        self._context.setModelVisible(True)
        self.strategy = BigWorld.CameraStrategyFreeFixable(self._context.mainMatrixProvider, self._context.getCurZoomlessOffset(), cameraSettings.freeFixableCamSpeed, CameraStateFreeFixable.PITCH_MIN, CameraStateFreeFixable.PITCH_MAX)
        self._context.cameraInstance.setStrategy(self.strategy, cameraSettings.freeFixableCamInterpolationTime)

    def rotationPower(self, rotationData):
        if self.strategy:
            self.strategy.horRotationPower = rotationData[0]
            self.strategy.vertRotationPower = rotationData[1]


class CameraStateSpectatorSide(CameraState):
    GROUND_NODE_UPDATE_TIME = 1.5

    def __init__(self):
        CameraState.__init__(self)
        self.__hpModel = BigWorld.Model('objects/camera_spectator.model')
        self.__cbExitState = None
        self.__returnToNormal = -1.0
        self.__lagHalfLife = 0.0
        self.__finishTime = 0.0
        self.__isNodeTimeline = False
        return

    def __parseData(self, data):
        if self.__cbExitState:
            BigWorld.cancelCallback(self.__cbExitState)
            self.__cbExitState = None
        if data.finishTime > 0.0:
            self.__finishTime = data.finishTime
            self.__cbExitState = BigWorld.callback(self.__finishTime, self._context.cameraManager.leaveState)
            self.__returnToNormal = data.finishLength
        if hasattr(data, 'lagHalfLife'):
            self.__lagHalfLife = data.lagHalfLife
        strategyData = {}
        self.__parseNodePositions(data, strategyData)
        self.__parseNodeTargets(data, strategyData)
        self.__parseFOVs(data, strategyData)
        self.__parsePositions(data, strategyData)
        self.__parseRotations(data, strategyData)
        self.__parseEffects(data, strategyData)
        if hasattr(data, 'linkingType'):
            strategyData['linkingType'] = data.linkingType
        else:
            LOG_ERROR("Linking type isn't exist!")
        return strategyData

    def __parseNodePositions(self, data, parsedData):
        if hasattr(data, 'nodePositionTimeline'):
            parsedData['nodePositions'] = self.__parseNodeTimeline(data.nodePositionTimeline)

    def __parseNodeTargets(self, data, parsedData):
        if hasattr(data, 'nodeTargetTimeline'):
            parsedData['nodeTargets'] = self.__parseNodeTimeline(data.nodeTargetTimeline)

    def __parseFOVs(self, data, parsedData):
        parsedData['fov'] = self.__parseFOVTimeline(data.fovTimeline)

    def __parsePositions(self, data, parsedData):
        if hasattr(data, 'positionTimeline'):
            parsedData['positions'] = self.__parsePositionTimeline(data.positionTimeline)

    def __parseRotations(self, data, parsedData):
        if hasattr(data, 'rotationTimeline'):
            parsedData['rotations'] = self.__parseRotationTimeline(data.rotationTimeline)

    def __parseEffects(self, data, parsedData):
        if hasattr(data, 'effectTimeline'):
            parsedData['effects'] = self.__parseEffectTimeline(data.effectTimeline)

    def __parsePositionTimeline(self, data):
        positionKeytimes = []
        for keytime in data.keytime:
            try:
                coord = keytime.position
                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                positionKeytimes.append((keytime.time,
                 coord,
                 0,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        return positionKeytimes

    def __parseRotationTimeline(self, data):
        rotationKeytimes = []
        for keytime in data.keytime:
            try:
                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                rotationKeytimes.append((keytime.time,
                 keytime.rotation,
                 0,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        return rotationKeytimes

    def __parseNodeTimeline(self, data):
        nodeKeytimes = []
        for keytime in data.keytime:
            try:
                from clientConsts import NODE_TIMELINE_NODE_FLAGS
                from clientConsts import NODE_TIMELINE_NEAREST_NODE
                flags = NODE_TIMELINE_NODE_FLAGS.NONE
                try:
                    coord = self.__hpModel.node(keytime.node).nodeLocalTransform.applyToOrigin() * WORLD_SCALING
                except:
                    x, y, z, flags = BigWorld.getCameraNode(keytime.node)
                    coord = Math.Vector3(x, y, z)

                fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
                fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
                nodeKeytimes.append((keytime.time,
                 coord,
                 flags,
                 keytime.type,
                 keytime.duration,
                 fadeinTime,
                 fadeoutTime))
            except:
                LOG_CURRENT_EXCEPTION()
                continue

        return nodeKeytimes

    def __parseFOVTimeline(self, data):
        fovKeytimes = []
        for keytime in data.keytime:
            fadeinTime = keytime.fadeinTime if hasattr(keytime, 'fadeinTime') else 0.0
            fadeoutTime = keytime.fadeoutTime if hasattr(keytime, 'fadeoutTime') else 0.0
            fovKeytimes.append((keytime.time,
             keytime.fov,
             keytime.duration,
             fadeinTime,
             fadeoutTime))

        return fovKeytimes

    def __parseEffectTimeline(self, data):
        effectKeytimes = []
        for keytime in data.keytime:
            weight = keytime.weight if hasattr(keytime, 'weight') else 1.0
            effectKeytimes.append((keytime.time,
             keytime.id,
             weight,
             keytime.enable))

        return effectKeytimes

    def enter(self, params = None):
        if params:
            animationData = self.__parseData(params)
            self.__isNodeTimeline = 'nodePositions' in animationData
            if not self.__isNodeTimeline:
                source = Math.Matrix()
                source.translation = Math.Vector3(0.0, 0.0, 0.0)
            else:
                source = self._context.mainMatrixProvider
            self._context.cameraInstance.parentMatrix = source
            self._context.cameraInstance.collisionCheckEnabled = self.__isNodeTimeline
            self.strategy = BigWorld.CameraStrategyCinematic(animationData, Math.Vector3(0.0, 1.0, 0.0), source, self.__cbExitState is None, self._context.cameraInstance.effectController, self.__lagHalfLife)
            self.strategy.staticNodeUpdateTime = self.__class__.GROUND_NODE_UPDATE_TIME
            self._context.cameraInstance.setStrategy(self.strategy, 0.0)
        return

    def exit(self):
        CameraState.exit(self)
        self.__clear()

    def __clear(self):
        if self.__cbExitState:
            BigWorld.cancelCallback(self.__cbExitState)
            self.__cbExitState = None
        self._context.cameraInstance.parentMatrix = self._context.mainMatrixProvider
        self._context.cameraInstance.collisionCheckEnabled = True
        self.__finishTime = 0.0
        return

    def reEnter(self, params = None):
        self.updateParams(params)

    def updateParams(self, params = None):
        self.__clear()
        self.enter(params)

    def getReturnToNormalTime(self):
        return self.__returnToNormal

    def setReturnToNormalTime(self, val):
        self.__returnToNormal = val

    def setCinematicTime(self, value):
        self.strategy.setTime(value)
        if self.__finishTime > 0.0:
            if value < self.__finishTime:
                leaveTime = self.__finishTime - value
                if self.__cbExitState:
                    BigWorld.cancelCallback(self.__cbExitState)
                self.__cbExitState = BigWorld.callback(leaveTime, self._context.cameraManager.leaveState)

    def updateTarget(self):
        if self.strategy:
            if self.__isNodeTimeline:
                newSource = self._context.mainMatrixProvider
                self.strategy.sourceMatrix = newSource
                self._context.cameraInstance.parentMatrix = newSource
        else:
            LOG_ERROR("Cannot update the target because the strategy isn't exist!")