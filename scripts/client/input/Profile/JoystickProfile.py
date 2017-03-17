# Embedded file name: scripts/client/input/Profile/JoystickProfile.py
import BigWorld
import math
import GameEnvironment
from ICMultiUpdate import ICMultiUpdate
import InputMapping
from MathExt import clamp, sign, FloatToCInt16
from _preparedBattleData_db import preparedBattleData
from consts import FORCE_AXIS, FLAPS_AXIS, HORIZONTAL_AXIS, VERTICAL_AXIS, ROLL_AXIS
from input.InputSubsystem.JoyInput import JoystickExpertInput
from input.InputSubsystem.KeyboardInput import KeyboardInput
from input.Profile.ProfileBase import IProfileBase
from clientConsts import NOT_CONTROLLED_MOD
from input.InputSubsystem.cameraOverlookInput import cameraOverlookInput
CAMERA_ROLL_SPEED = 5.0
CAMERA_YAW_SPEED = 8.0
CAMERA_PITCH_SPEED = 10

class JoystickProfile(IProfileBase, ICMultiUpdate):

    def __init__(self, inputAxis, notControlledByUser):
        self._notControlledByUser = notControlledByUser
        self._forciblySendAxis = False
        self.__overlookCameraInput = cameraOverlookInput()
        InputMapping.g_instance.onSaveControls += self._onSaveControls
        GameEnvironment.getCamera().eZoomStateChanged += self.__zoomStateChanged
        ICMultiFunction = lambda : (self.__autopilotUpdate() if self._notControlledByUser else None)
        ICMultiUpdate.__init__(self, (0.1, ICMultiFunction))
        self.__axisKeyBoard = [0.0] * 5
        self.__axisJoy = [0.0] * 5
        self.__lastAxis = [0.0] * 5
        self._isSlipComp = False
        self.__joystick = JoystickExpertInput(self)
        self.__joystick.pushLastEvent()
        self.__keyboard = KeyboardInput(self)
        self.__keyboard.isMultiplySignal = False
        self._onSaveControls()

    def getCurrentForce(self):
        return self.__lastAxis[FORCE_AXIS]

    def dispose(self):
        InputMapping.g_instance.onSaveControls -= self._onSaveControls
        GameEnvironment.getCamera().eZoomStateChanged -= self.__zoomStateChanged
        ICMultiUpdate.dispose(self)
        self.__joystick.dispose()
        self.__keyboard.dispose()
        self.__overlookCameraInput.dispose()
        self.__joystick = None
        self.__keyboard = None
        self.__overlookCameraInput = None
        return

    def restart(self):
        ICMultiUpdate.restart(self)

    def _onSaveControls(self):
        settings = InputMapping.g_instance.mouseSettings
        camera = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyNormal']
        cameraInertia = settings.INERTIA_CAMERA
        cameraInertiaRoll = settings.INERTIA_CAMERA_ROLL
        camera.speedRoll = CAMERA_ROLL_SPEED + 2.0 * CAMERA_ROLL_SPEED * (1.0 - cameraInertiaRoll) if cameraInertiaRoll > 0 else 100
        camera.speedYaw = CAMERA_YAW_SPEED + 2.0 * CAMERA_YAW_SPEED * (1.0 - cameraInertia) if cameraInertia > 0 else 100
        camera.speedPitch = CAMERA_PITCH_SPEED + 2.0 * CAMERA_PITCH_SPEED * (1.0 - cameraInertia) if cameraInertia > 0 else 100
        flex = lambda x, min_, max_: (max_ - min_) * math.pow(x, 2.0) * math.exp(x - 1) + min_
        self.__overlookCameraInput.setTurnSpeed(flex(settings.HATKA_MOVE_SPEED, 100, 400))
        camera.flexibility = flex(1.0 - settings.HATKA_MOVE_SPEED, 1e-15, 0.0001)
        self._isSlipComp = settings.SLIP_COMPENSATION_VALUE
        BigWorld.player().cell.sendLiningFlag(int(clamp(0.0, settings.SLIP_COMPENSATION_VALUE * 255, 255)))
        BigWorld.player().cell.sendJoyVersionFlag(settings.JOY_VERSION_SWITCHER)
        self.__joystick.pushLastEvent()

    def __resendRudders(self):
        self._forciblySendAxis = True
        for axis in range(0, len(self.__axisKeyBoard)):
            self.__send(axis)

        self._forciblySendAxis = False

    def __zoomStateChanged(self, newState):
        self.__resendRudders()

    def __sensitivity(self, axis):
        if GameEnvironment.getCamera().isSniperMode and axis in (HORIZONTAL_AXIS, VERTICAL_AXIS):
            sensitivityInSniperMode = InputMapping.g_instance.mouseSettings.SENSITIVITY_IN_SNIPER_MODE
            return max(0.1, sensitivityInSniperMode)
        return 1.0

    def __send(self, axis):
        player = BigWorld.player()
        value = self.__sensitivity(axis) * self.__axisJoy[axis] * (1.0 - abs(self.__axisKeyBoard[axis])) + self.__axisKeyBoard[axis]
        if self.__lastAxis[axis] != value or self._forciblySendAxis:
            player.cell.sendInputJoyAxis(axis, FloatToCInt16(value))
            player.applyInputAxis(axis, value)
            self.__lastAxis[axis] = value

    def sendAxis(self, axis, value):
        self.__axisKeyBoard[axis] = value
        if self._notControlledByUser:
            if self._notControlledByUser & NOT_CONTROLLED_MOD.PLANE_ALIGN and axis in (FLAPS_AXIS, FORCE_AXIS):
                self.__send(axis)
            return
        self.__send(axis)

    def sendPrimaryAxis(self, axis, value, axisID):
        self.__axisJoy[axis] = value
        if self._notControlledByUser:
            if self._notControlledByUser & NOT_CONTROLLED_MOD.PLANE_ALIGN and axis in (FLAPS_AXIS, FORCE_AXIS):
                self.__send(axis)
            return
        self.__send(axis)

    def notControlledByUser(self, value):
        self._notControlledByUser = value
        if not self._notControlledByUser:
            self.__resendRudders()

    def processMouseEvent(self, event):
        self.__overlookCameraInput.processMouseEvent(event)

    def processJoystickEvent(self, event):
        self.__joystick.processJoystickEvent(event)
        self.__overlookCameraInput.processJoystickEvent(event)

    def addCommandListeners(self, processor):
        self.__keyboard.addCommandListeners(processor)
        self.__overlookCameraInput.addCommandListeners(processor)

    def removeCommandListeners(self, processor):
        self.__keyboard.removeCommandListeners(processor)
        self.__overlookCameraInput.removeCommandListeners(processor)

    def slipCompensationVisualisation(self):
        if self._isSlipComp and not self._notControlledByUser:
            owner = BigWorld.player()
            fmRotation = owner.getRotation()
            speedDirection = owner.getWorldVector()
            speedDirection.normalise()
            dotX = clamp(-1.0, fmRotation.getAxisX().dot(speedDirection), 1.0)
            dotY = clamp(-1.0, fmRotation.getAxisY().dot(speedDirection), 1.0)
            angleX = abs(math.pi / 2.0 - math.acos(dotX)) / math.radians(10.0)
            angleY = abs(math.pi / 2.0 - math.acos(dotY)) / math.radians(35.0 / 2.0)
            signX = sign(dotX)
            signY = sign(dotY)
            hAxis = clamp(-1.0, self.__lastAxis[HORIZONTAL_AXIS] - self._isSlipComp * (1.0 - abs(self.__lastAxis[HORIZONTAL_AXIS])) * clamp(-1.0, signX * angleX, 1.0), 1.0)
            owner.applyInputAxis(HORIZONTAL_AXIS, hAxis)
            vAxis = clamp(-1.0, self.__lastAxis[VERTICAL_AXIS] - self._isSlipComp * (1.0 - abs(self.__lastAxis[VERTICAL_AXIS])) * clamp(-1.0, signY * angleY, 1.0), 1.0)
            owner.applyInputAxis(VERTICAL_AXIS, vAxis)

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