# Embedded file name: scripts/client/input/Profile/GamepadProfile.py
import math
import BigWorld
from EntityHelpers import EntityStates
from Camera import CameraState
import GameEnvironment
from ICMultiUpdate import ICMultiUpdate
import InputMapping
import Math
from MathExt import clamp, sign, FloatToCInt8, FloatToUCInt8, FloatToCInt16
from consts import HORIZONTAL_AXIS, ROLL_AXIS, VERTICAL_AXIS, FLAPS_AXIS, FORCE_AXIS
from input.InputSubsystem.KeyboardInput import KeyboardInput
from input.InputSubsystem.GamepadInput import GamepadInput
from input.Profile.ProfileBase import IProfileBase
from clientConsts import NOT_CONTROLLED_MOD, AXIS_MUTE_MOD

class GamepadProfile(IProfileBase, ICMultiUpdate):

    def __init__(self, inputAxis, notControlledByUser, currentBattleMode):
        self.__axisKeyBoard = [0.0] * 5
        self.__lastAxis = [0.0] * 5
        self.__axisJoy = [0.0] * 5
        self.__lastKeyBoardAxis = [0.0] * 5
        self.__resetAxis()
        self._notControlledByUser = notControlledByUser
        self.__battleMode = currentBattleMode
        self.__spline = None
        self.__smoothSpline = None
        self.__gamePad = GamepadInput(self)
        self.__keyboard = KeyboardInput(self)
        self.__keyboard.isMultiplySignal = False
        self._onSaveControls()
        self.__camDirection = Math.Vector3()
        self.__muted = AXIS_MUTE_MOD.NO_MUTE
        InputMapping.g_instance.onSaveControls += self._onSaveControls
        GameEnvironment.getInput().eBattleModeChange += self.__eBattleModeChange
        ICMultiFunction = lambda : (self.__autopilotUpdate() if self._notControlledByUser else None)
        ICMultiUpdate.__init__(self, (0.1, self.__updateVisibleAxis), (0.1, ICMultiFunction))
        return

    def dispose(self):
        ICMultiUpdate.dispose(self)
        self.__gamePad.dispose()
        self.__keyboard.dispose()
        self.__gamePad = None
        self.__keyboard = None
        freeState = GameEnvironment.getCamera().stateObject(CameraState.Free)
        if freeState:
            freeState.setInvertVertical(False)
        InputMapping.g_instance.onSaveControls -= self._onSaveControls
        GameEnvironment.getInput().eBattleModeChange -= self.__eBattleModeChange
        return

    def restart(self):
        ICMultiUpdate.restart(self)
        self.__gamePad.restart()
        self.__keyboard.restart()

    def __eBattleModeChange(self, value):
        BigWorld.player().cell.sendDirectionalMouseMode(value)
        self.__battleMode = value

    @property
    def battleMode(self):
        return self.__battleMode

    def notControlledByUser(self, value):
        self._notControlledByUser = value
        self.__gamePad.notControlledByUser(value)
        if not value:
            for axis in range(0, len(self.__axisKeyBoard)):
                self.__send(axis)

    def _onSaveControls(self):
        jSet = InputMapping.g_instance.joystickSettings
        spline = type('splineDummy', (), {'p': [Math.Vector2(0.0, 1.0), Math.Vector2(1.0, 1.0)],
         'pointCount': 100})
        self.__setMouseSpline(spline)
        splineArgs = (list(spline.p), spline.pointCount)
        combatStrategy = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyMouse']
        rudderZone = 0.5 * BigWorld.projection().fov
        minSensitivity = 1e-06
        maxSensitivity = 0.01
        x = jSet.CAMERA_FLEXIBILITY
        if jSet.CAMERA_TYPE == 0:
            combatStrategy.behaviorHorizon = 1
            BigWorld.player().cell.sendCameraModType(1)
        elif jSet.CAMERA_TYPE == 2:
            combatStrategy.behaviorHorizon = 2
            BigWorld.player().cell.sendCameraModType(2)
        else:
            raise
        combatStrategy.reset()
        combatStrategy.cameraRollSpeed = math.radians(300.0) * jSet.CAMERA_ROLL_SPEED + math.radians(60.0)
        combatStrategy.cameraAngle = math.radians(90.0) * jSet.CAMERA_ANGLE
        combatStrategy.flexibility = (maxSensitivity - minSensitivity) * math.pow(x, 2.0) * math.exp(x - 1) + minSensitivity
        combatStrategy.accelerationTime = 1.0 + 1.9 * jSet.CAMERA_ACCELERATION
        combatStrategy.maxStuckAngle = rudderZone
        combatStrategy.setMouseIntensitySpline(splineArgs)
        BigWorld.player().cell.sendAutomaticFlapsChanged(jSet.AUTOMATIC_FLAPS)
        BigWorld.player().cell.sendFlipFlag(jSet.SHIFT_TURN)
        BigWorld.player().cell.sendInputSimpleMode(jSet.SAFE_ROLL_ON_LOW_ALTITUDE)
        BigWorld.player().cell.sendRollSpeedCfc(FloatToUCInt8(1.0 * jSet.ROLL_SPEED_CFC + 0.0))
        BigWorld.player().cell.sendIntensityAlignmentInCenter(FloatToUCInt8(jSet.EQUALIZER_FORCE))
        BigWorld.player().cell.sendTrackingCamera(InputMapping.g_instance.mouseSettings.ALLOW_LEAD)

    def __setMouseSpline(self, spline):
        self.__spline = Math.Curve(list(spline.p), spline.pointCount)
        self.__smoothSpline = Math.Curve([Math.Vector2(0.0, spline.p[-1].y), Math.Vector2(1.0, 1.0)], 10)
        self.__spline.refresh()
        self.__smoothSpline.refresh()

    def getMouseIntensity(self, cAngle, mAngle):
        if self.__spline is not None and self.__smoothSpline is not None:
            if cAngle > mAngle:
                return self.__smoothSpline.calc(min(cAngle / (0.5 * (mAngle + math.pi)), 1.0))
            return self.__spline.calc(cAngle / mAngle)
        else:
            return 0.0
            return

    def sendAxis(self, axis, value):
        self.__axisKeyBoard[axis] = value
        if self._notControlledByUser:
            if self._notControlledByUser & NOT_CONTROLLED_MOD.PLANE_ALIGN and axis in (FLAPS_AXIS, FORCE_AXIS):
                self.__send(axis)
            return
        self.__send(axis)

    def sendPrimaryAxis(self, axis, value):
        self.__axisJoy[axis] = value
        if self._notControlledByUser:
            if self._notControlledByUser & NOT_CONTROLLED_MOD.PLANE_ALIGN and axis in (FLAPS_AXIS, FORCE_AXIS):
                self.__send(axis)
            return
        self.__send(axis)

    def __send(self, axis):
        if self.__muted != AXIS_MUTE_MOD.NO_MUTE:
            return
        value = self.__axisJoy[axis] * (1.0 - abs(self.__axisKeyBoard[axis])) + self.__axisKeyBoard[axis]
        if self.__lastKeyBoardAxis[axis] != value:
            BigWorld.player().cell.sendInputAxis(axis, FloatToCInt8(value))
            self.__lastKeyBoardAxis[axis] = value

    def addCommandListeners(self, processor):
        self.__gamePad.addCommandListeners(processor)
        self.__keyboard.addCommandListeners(processor)

    def removeCommandListeners(self, processor):
        self.__gamePad.removeCommandListeners(processor)
        self.__keyboard.removeCommandListeners(processor)

    def processMouseEvent(self, event):
        pass

    def processJoystickEvent(self, event):
        self.__gamePad.processJoystickEvent(event)

    def getCurrentForce(self):
        return self.__lastKeyBoardAxis[FORCE_AXIS]

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
            fmRotation = BigWorld.player().getRotation()
            norm = Math.Vector3(self.__camDirection)
            norm.normalise()
            yawAngle = 0.5 * math.pi - math.acos(clamp(-1.0, fmRotation.getAxisX().dot(norm), 1.0))
            pitchAngle = 0.5 * math.pi - math.acos(clamp(-1.0, fmRotation.getAxisY().dot(norm), 1.0))
            mouseRoll = -sign(yawAngle) * clamp(-1.0, max(0.0, abs(yawAngle) / math.radians(5.0) - 1.0), 1.0)
            hAxis = clamp(-1.0, yawAngle / math.radians(5.0) * 8.0, 1.0) * (1 - abs(self.__lastKeyBoardAxis[HORIZONTAL_AXIS])) + self.__lastKeyBoardAxis[HORIZONTAL_AXIS]
            vAxis = clamp(-1.0, pitchAngle / math.radians(10.0), 1.0) * (1 - abs(self.__lastKeyBoardAxis[VERTICAL_AXIS])) + self.__lastKeyBoardAxis[VERTICAL_AXIS]
            rAxis = bool(InputMapping.g_instance.mouseSettings.ROLL_SPEED_CFC) * mouseRoll * (1 - abs(self.__lastKeyBoardAxis[ROLL_AXIS])) + self.__lastKeyBoardAxis[ROLL_AXIS]
            speedDirection = player.getWorldVector()
            speedDirection.normalise()
            dotX = clamp(-1.0, fmRotation.getAxisX().dot(speedDirection), 1.0)
            dotY = clamp(-1.0, fmRotation.getAxisY().dot(speedDirection), 1.0)
            angleX = abs(0.5 * math.pi - math.acos(dotX)) / math.radians(10.0)
            angleY = abs(0.5 * math.pi - math.acos(dotY)) / math.radians(35.0 / 2.0)
            signX = sign(dotX)
            signY = sign(dotY)
            hAxis = clamp(-1.0, hAxis - (1.0 - abs(hAxis)) * clamp(-1.0, signX * angleX, 1.0), 1.0)
            vAxis = clamp(-1.0, vAxis - (1.0 - abs(vAxis)) * clamp(-1.0, signY * angleY, 1.0), 1.0)
            mouseAngle = math.acos(clamp(-1.0, fmRotation.getAxisZ().dot(norm), 1.0))
            equalizerAngle = 0.5 * (0.3 + 0.7 * InputMapping.g_instance.mouseSettings.RADIUS_OF_CONDUCTING) * BigWorld.projection().fov * InputMapping.g_instance.mouseSettings.EQUALIZER_ZONE_SIZE
            equalizer = max(0.0, (equalizerAngle - mouseAngle) / equalizerAngle) * clamp(-1.0, 3.0 * bool(InputMapping.g_instance.mouseSettings.EQUALIZER_FORCE) * player.roll / math.pi, 1.0) if equalizerAngle else 0.0
            rAxis = clamp(-1.0, rAxis - (1.0 - abs(rAxis)) * equalizer, 1.0)
            self.__applyInputAxis(HORIZONTAL_AXIS, clamp(-1.0, hAxis, 1.0))
            self.__applyInputAxis(ROLL_AXIS, clamp(-1.0, rAxis, 1.0))
            self.__applyInputAxis(VERTICAL_AXIS, clamp(-1.0, vAxis, 1.0))
            self.__applyInputAxis(FORCE_AXIS, self.__lastKeyBoardAxis[FORCE_AXIS])
            automaticFlaps = False
            if InputMapping.g_instance.mouseSettings.AUTOMATIC_FLAPS:
                automaticFlaps = int(max(0.0, player.asymptoteVMaxPitch - abs(player.getRotationSpeed().y)) < 0.25 * player.asymptoteVMaxPitch)
            self.__applyInputAxis(FLAPS_AXIS, self.__lastKeyBoardAxis[FLAPS_AXIS] or automaticFlaps)

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
                owner.applyInputAxis(ROLL_AXIS, -rollAxis)
            pitchAxis = owner.pitch
            pitchAxis = min(1.0, max(-1.0, pitchAxis))
            owner.applyInputAxis(VERTICAL_AXIS, pitchAxis)
            owner.applyInputAxis(HORIZONTAL_AXIS, 0)
            owner.applyInputAxis(FORCE_AXIS, self.__lastKeyBoardAxis[FORCE_AXIS])
            automaticFlaps = False
            if InputMapping.g_instance.mouseSettings.AUTOMATIC_FLAPS:
                automaticFlaps = int(max(0.0, owner.asymptoteVMaxPitch - abs(owner.getRotationSpeed().y)) < 0.25 * owner.asymptoteVMaxPitch)
            owner.applyInputAxis(FLAPS_AXIS, self.__lastKeyBoardAxis[FLAPS_AXIS] or automaticFlaps)

    def mute(self, value):
        self.__muted = value