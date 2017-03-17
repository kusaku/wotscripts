# Embedded file name: scripts/client/input/Profile/MouseProfile.py
import math
import BigWorld
from EntityHelpers import EntityStates
from Camera import CameraState
import GameEnvironment
from ICMultiUpdate import ICMultiUpdate
import InputMapping
import Math
from MathExt import clamp, sign, FloatToCInt8, FloatToUCInt8, FloatToCInt16, FloatArrayToTupleOfCInt8, TupleOfCInt8ToFloatArray
import Settings
from consts import HORIZONTAL_AXIS, ROLL_AXIS, VERTICAL_AXIS, FLAPS_AXIS, FORCE_AXIS
from input.InputSubsystem.MouseInput import MouseCursorDirection, MousePlaneDirection
from input.InputSubsystem.KeyboardInput import KeyboardInput
from input.Profile.ProfileBase import IProfileBase
from clientConsts import NOT_CONTROLLED_MOD

class CAMERA_STRATEGY:
    LOCAL = 0
    WORLD = 1


class MouseProfile(IProfileBase, ICMultiUpdate):

    def __init__(self, inputAxis, notControlledByUser, currentBattleMode):
        self.__mouseList = [MousePlaneDirection, MouseCursorDirection]
        self.__axisKeyBoard = [0.0] * 5
        self.__lastAxis = [0.0] * 5
        self.__lastKeyBoardAxis = [0.0] * 5
        self.__resetAxis()
        self._notControlledByUser = notControlledByUser
        self.__battleMode = currentBattleMode
        self.__spline = None
        self.__smoothSpline = None
        self.__processor = None
        self.__mouse = self.__mouseList[CAMERA_STRATEGY.WORLD](self)
        self.__keyboard = KeyboardInput(self)
        self.__keyboard.isMultiplySignal = False
        self._onSaveControls()
        self.__camDirection = Math.Vector3()
        InputMapping.g_instance.onSaveControls += self._onSaveControls
        GameEnvironment.getInput().eBattleModeChange += self.__eBattleModeChange
        ICMultiFunction = lambda : (self.__autopilotUpdate() if self._notControlledByUser else None)
        ICMultiUpdate.__init__(self, (0.1, self.__updateVisibleAxis), (0.1, ICMultiFunction))
        return

    def dispose(self):
        ICMultiUpdate.dispose(self)
        self.__mouse.dispose()
        self.__keyboard.dispose()
        self.__mouse = None
        self.__keyboard = None
        freeState = GameEnvironment.getCamera().stateObject(CameraState.Free)
        if freeState:
            freeState.setInvertVertical(False)
        InputMapping.g_instance.onSaveControls -= self._onSaveControls
        GameEnvironment.getInput().eBattleModeChange -= self.__eBattleModeChange
        return

    def restart(self):
        ICMultiUpdate.restart(self)
        self.__mouse.restart()
        self.__keyboard.restart()

    def __eBattleModeChange(self, value):
        BigWorld.player().cell.sendDirectionalMouseMode(value)
        self.__battleMode = value

    @property
    def battleMode(self):
        return self.__battleMode

    def notControlledByUser(self, value):
        self._notControlledByUser = value
        self.__mouse.notControlledByUser(value)
        if not value:
            for axis in range(0, len(self.__axisKeyBoard)):
                self.__send(axis)

    def _onSaveControls(self):
        camType = InputMapping.g_instance.mouseSettings.CAMERA_TYPE
        MouseCombatStrategy = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse']
        rudderZone = 0.5 * (0.3 + 0.7 * InputMapping.g_instance.mouseSettings.RADIUS_OF_CONDUCTING) * BigWorld.projection().fov
        minSensitivity = 1e-06
        maxSensitivity = 0.01
        x = InputMapping.g_instance.mouseSettings.CAMERA_FLEXIBILITY
        GameEnvironment.getCamera().stateObject(CameraState.Free).setInvertVertical(InputMapping.g_instance.primarySettings.MOUSE_INVERT_VERT)
        if camType == 1:
            self.__switchMouseInput(self.__mouseList[CAMERA_STRATEGY.LOCAL])
            MouseCombatStrategy.behaviorHorizon = 0
            BigWorld.player().cell.sendCameraModType(0)
        elif camType == 0:
            MouseCombatStrategy.behaviorHorizon = 1
            self.__switchMouseInput(self.__mouseList[CAMERA_STRATEGY.WORLD])
            BigWorld.player().cell.sendCameraModType(1)
        elif camType == 2:
            MouseCombatStrategy.behaviorHorizon = 2
            self.__switchMouseInput(self.__mouseList[CAMERA_STRATEGY.WORLD])
            BigWorld.player().cell.sendCameraModType(2)
        else:
            raise
        spline = InputMapping.g_instance.mouseSettings.MOUSE_INTENSITY_SPLINE
        self.__setMouseSpline(spline)
        splineArgs = (list(spline.p), spline.pointCount)
        MouseCombatStrategy.reset()
        MouseCombatStrategy.cameraRollSpeed = math.radians(300.0) * InputMapping.g_instance.primarySettings.CAMERA_ROLL_SPEED + math.radians(60.0)
        MouseCombatStrategy.cameraAngle = math.radians(90.0) * InputMapping.g_instance.primarySettings.CAMERA_ANGLE
        MouseCombatStrategy.flexibility = (maxSensitivity - minSensitivity) * math.pow(x, 2.0) * math.exp(x - 1) + minSensitivity
        MouseCombatStrategy.accelerationTime = 0.1 + 1.9 * InputMapping.g_instance.mouseSettings.CAMERA_ACCELERATION
        MouseCombatStrategy.maxStuckAngle = rudderZone
        MouseCombatStrategy.setMouseIntensitySpline(splineArgs)
        self.__mouse.window = 1
        BigWorld.player().cell.sendAutomaticFlapsChanged(InputMapping.g_instance.mouseSettings.AUTOMATIC_FLAPS)
        BigWorld.player().cell.sendFlipFlag(InputMapping.g_instance.mouseSettings.SHIFT_TURN)
        BigWorld.player().cell.sendInputSimpleMode(InputMapping.g_instance.mouseSettings.SAFE_ROLL_ON_LOW_ALTITUDE)
        BigWorld.player().cell.sendRollSpeedCfc(FloatToUCInt8(1.0 * InputMapping.g_instance.mouseSettings.ROLL_SPEED_CFC + 0.0))
        BigWorld.player().cell.sendIntensityAlignmentInCenter(FloatToUCInt8(InputMapping.g_instance.mouseSettings.EQUALIZER_FORCE))
        BigWorld.player().cell.sendTrackingCamera(InputMapping.g_instance.mouseSettings.ALLOW_LEAD)
        BigWorld.player().cell.sendMixingMethod(InputMapping.g_instance.mouseSettings.METHOD_OF_MIXING)
        self.__mouse.restart()

    def __setMouseSpline(self, spline):
        self.__spline = Math.Curve(list(spline.p), spline.pointCount)
        frontPoint = Math.Vector2(0.0, spline.p[-1].y)
        beckPoint = Math.Vector2(1.0, 1.0) if frontPoint.y else Math.Vector2(1.0, 0.0)
        self.__smoothSpline = Math.Curve([frontPoint, beckPoint], 10)
        self.__spline.refresh()
        self.__smoothSpline.refresh()

    def getMouseIntensity(self, cAngle, mAngle):
        if self.__spline is not None and self.__smoothSpline is not None:
            if cAngle > mAngle:
                return clamp(0.0, self.__smoothSpline.calc(min(cAngle / (0.5 * (mAngle + math.pi)), 1.0)), 1.0)
            return clamp(0.0, self.__spline.calc(cAngle / mAngle), 1.0)
        else:
            return 0.0
            return

    def __switchMouseInput(self, newMouse):
        if self.__processor is not None:
            self.__mouse.removeCommandListeners(self.__processor)
        self.__mouse.dispose()
        self.__mouse = newMouse(self)
        if self.__processor is not None:
            self.__mouse.addCommandListeners(self.__processor)
        return

    def sendAxis(self, axis, value):
        self.__axisKeyBoard[axis] = value
        if self._notControlledByUser:
            if self._notControlledByUser & NOT_CONTROLLED_MOD.PLANE_ALIGN and axis in (FLAPS_AXIS, FORCE_AXIS):
                self.__send(axis)
            return
        self.__send(axis)

    def __send(self, axis):
        value = self.__axisKeyBoard[axis]
        if self.__lastKeyBoardAxis[axis] != value:
            BigWorld.player().cell.sendInputAxis(axis, FloatToCInt8(value))
            self.__lastKeyBoardAxis[axis] = value

    def addCommandListeners(self, processor):
        if self.__processor is None:
            self.__processor = processor
        self.__mouse.addCommandListeners(processor)
        self.__keyboard.addCommandListeners(processor)
        return

    def removeCommandListeners(self, processor):
        if self.__processor is not None:
            self.__processor = None
        self.__mouse.removeCommandListeners(processor)
        self.__keyboard.removeCommandListeners(processor)
        return

    def processMouseEvent(self, event):
        self.__mouse.processMouseEvent(event)

    def processJoystickEvent(self, event):
        pass

    def getCurrentForce(self):
        return self.__axisKeyBoard[FORCE_AXIS]

    def setCamDirection(self, value):
        self.__camDirection = value

    def __resetAxis(self):
        player = BigWorld.player()
        player.applyInputAxis(ROLL_AXIS, 0.0)
        player.applyInputAxis(HORIZONTAL_AXIS, 0.0)
        player.applyInputAxis(VERTICAL_AXIS, 0.0)
        player.applyInputAxis(FORCE_AXIS, 0.0)
        player.applyInputAxis(FLAPS_AXIS, 0.0)

    def __updateVisibleAxis(self):
        if not self._notControlledByUser and EntityStates.inState(BigWorld.player(), EntityStates.GAME):
            player = BigWorld.player()
            direction = self.__camDirection
            fmRotation = BigWorld.player().getRotation()
            rotation = Math.Quaternion(fmRotation)
            rotation.invert()
            norm = Math.Vector3(direction)
            norm.normalise()
            yawAngle = math.pi / 2.0 - math.acos(clamp(-1.0, fmRotation.getAxisX().dot(norm), 1.0))
            pitchAngle = math.pi / 2.0 - math.acos(clamp(-1.0, fmRotation.getAxisY().dot(norm), 1.0))
            mouseRoll = -sign(yawAngle) * clamp(-1.0, max(0.0, (abs(yawAngle) - math.radians(5.0)) / math.radians(5.0)), 1.0)
            hAxis = clamp(-1.0, yawAngle / math.radians(5.0) * 8.0, 1.0) * (1 - abs(self.__axisKeyBoard[HORIZONTAL_AXIS])) + self.__axisKeyBoard[HORIZONTAL_AXIS]
            vAxis = clamp(-1.0, pitchAngle / math.radians(10.0), 1.0) * (1 - abs(self.__axisKeyBoard[VERTICAL_AXIS])) + self.__axisKeyBoard[VERTICAL_AXIS]
            roll_cfc = bool(InputMapping.g_instance.mouseSettings.ROLL_SPEED_CFC) * max(0.25, 1.0 - (1.0 - InputMapping.g_instance.mouseSettings.ROLL_SPEED_CFC) ** 3)
            rAxis = roll_cfc * mouseRoll * (1 - abs(self.__axisKeyBoard[ROLL_AXIS])) + self.__axisKeyBoard[ROLL_AXIS]
            speedDirection = player.getWorldVector()
            speedDirection.normalise()
            dotX = clamp(-1.0, fmRotation.getAxisX().dot(speedDirection), 1.0)
            dotY = clamp(-1.0, fmRotation.getAxisY().dot(speedDirection), 1.0)
            angleX = abs(math.pi / 2.0 - math.acos(dotX)) / math.radians(10.0)
            angleY = abs(math.pi / 2.0 - math.acos(dotY)) / math.radians(35.0 / 2.0)
            signX = sign(dotX)
            signY = sign(dotY)
            hAxis = clamp(-1.0, hAxis - (1.0 - abs(hAxis)) * clamp(-1.0, signX * angleX, 1.0), 1.0)
            vAxis = clamp(-1.0, vAxis - (1.0 - abs(vAxis)) * clamp(-1.0, signY * angleY, 1.0), 1.0)
            mouseAngle = math.acos(clamp(-1.0, fmRotation.getAxisZ().dot(norm), 1.0))
            equalizerAngle = 0.5 * (0.3 + 0.7 * InputMapping.g_instance.mouseSettings.RADIUS_OF_CONDUCTING) * BigWorld.projection().fov * InputMapping.g_instance.mouseSettings.EQUALIZER_ZONE_SIZE
            equalizer = max(0.0, 1.0 - mouseAngle / equalizerAngle) * clamp(-1.0, InputMapping.g_instance.mouseSettings.EQUALIZER_FORCE * player.roll / player.rollRudderNorma, 1.0) if equalizerAngle else 0.0
            rAxis = clamp(-1.0, rAxis - (1.0 - abs(rAxis)) * equalizer, 1.0)
            self.__applyInputAxis(HORIZONTAL_AXIS, clamp(-1.0, hAxis, 1.0))
            self.__applyInputAxis(ROLL_AXIS, clamp(-1.0, rAxis, 1.0))
            self.__applyInputAxis(VERTICAL_AXIS, clamp(-1.0, vAxis, 1.0))
            self.__applyInputAxis(FORCE_AXIS, self.__axisKeyBoard[FORCE_AXIS])
            automaticFlaps = False
            if InputMapping.g_instance.mouseSettings.AUTOMATIC_FLAPS:
                automaticFlaps = int(max(0.0, player.asymptoteVMaxPitch - abs(player.getRotationSpeed().y)) < 0.25 * player.asymptoteVMaxPitch)
            self.__applyInputAxis(FLAPS_AXIS, self.__axisKeyBoard[FLAPS_AXIS] or automaticFlaps)

    def __applyInputAxis(self, axis, value):
        if self.__lastAxis[axis] != value:
            BigWorld.player().applyInputAxis(axis, value)
            self.__lastAxis[axis] = value

    def __autopilotUpdate(self):
        """successor should provide an update of this method through its own ICMultiUpdate """
        if self._notControlledByUser & (NOT_CONTROLLED_MOD.NCBU_STRATEGY_ACTIVATE | NOT_CONTROLLED_MOD.AUTOPILOT):
            owner = BigWorld.player()
            if abs(owner.pitch) < 0.25 * math.pi:
                rollAxis = owner.roll * 0.5
                rollAxis = min(1.0, max(-1.0, rollAxis))
                self.__applyInputAxis(ROLL_AXIS, -rollAxis)
            pitchAxis = owner.pitch
            pitchAxis = min(1.0, max(-1.0, pitchAxis))
            self.__applyInputAxis(VERTICAL_AXIS, pitchAxis)
            self.__applyInputAxis(HORIZONTAL_AXIS, 0)
            axisKeyBoard = {FORCE_AXIS: 0,
             FLAPS_AXIS: 0}
            if not self._notControlledByUser & NOT_CONTROLLED_MOD.AUTOPILOT:
                axisKeyBoard[FORCE_AXIS] = self.__axisKeyBoard[FORCE_AXIS]
                axisKeyBoard[FLAPS_AXIS] = self.__axisKeyBoard[FLAPS_AXIS]
            self.__applyInputAxis(FORCE_AXIS, axisKeyBoard[FORCE_AXIS])
            automaticFlaps = False
            if InputMapping.g_instance.mouseSettings.AUTOMATIC_FLAPS:
                automaticFlaps = int(max(0.0, owner.asymptoteVMaxPitch - abs(owner.getRotationSpeed().y)) < 0.25 * owner.asymptoteVMaxPitch)
            self.__applyInputAxis(FLAPS_AXIS, axisKeyBoard[FLAPS_AXIS] or automaticFlaps)