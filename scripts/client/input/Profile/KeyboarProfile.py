# Embedded file name: scripts/client/input/Profile/KeyboarProfile.py
import BigWorld
import Math
import GameEnvironment
import math
from ICMultiUpdate import ICMultiUpdate
import InputMapping
from MathExt import clamp, sign, FloatToCInt8
from consts import FORCE_AXIS, FLAPS_AXIS, HORIZONTAL_AXIS, VERTICAL_AXIS, ROLL_AXIS
from input.InputSubsystem.KeyboardInput import KeyboardInput
from input.Profile.ProfileBase import IProfileBase
from clientConsts import NOT_CONTROLLED_MOD
CAMERA_ROLL_SPEED = 5.0
CAMERA_YAW_SPEED = 8.0
CAMERA_PITCH_SPEED = 10

class KeyboardProfile(IProfileBase, ICMultiUpdate):

    def __init__(self, inputAxis, notControlledByUser):
        self._notControlledByUser = notControlledByUser
        self._forciblySendAxis = False
        InputMapping.g_instance.onSaveControls += self._onSaveControls
        ICMultiFunction = lambda : (self.__autopilotUpdate() if self._notControlledByUser else None)
        ICMultiUpdate.__init__(self, (0.1, ICMultiFunction))
        self.__axisKeyBoard = [0.0] * 5
        self.__lastAxis = [0.0] * 5
        self.__isSlipComp = InputMapping.g_instance.mouseSettings.SLIP_COMPENSATION
        self.__keyboard = KeyboardInput(self)
        self._onSaveControls()

    def dispose(self):
        InputMapping.g_instance.onSaveControls -= self._onSaveControls
        ICMultiUpdate.dispose(self)
        self.__keyboard.dispose()
        self.__keyboard = None
        return

    def __send(self, axis):
        value = self.__axisKeyBoard[axis]
        player = BigWorld.player()
        if self.__lastAxis[axis] != value or self._forciblySendAxis:
            player.cell.sendInputAxis(axis, FloatToCInt8(value))
            player.applyInputAxis(axis, value)
            self.__lastAxis[axis] = value

    def sendAxis(self, axis, value):
        self.__axisKeyBoard[axis] = value
        if self._notControlledByUser:
            if self._notControlledByUser & NOT_CONTROLLED_MOD.PLANE_ALIGN and axis in (FLAPS_AXIS, FORCE_AXIS):
                self.__send(axis)
            return
        self.__send(axis)

    def notControlledByUser(self, value):
        self._notControlledByUser = value
        if not value:
            self._forciblySendAxis = True
            for axis in range(0, len(self.__axisKeyBoard)):
                self.__send(axis)

            self._forciblySendAxis = False

    def processMouseEvent(self, event):
        pass

    def processJoystickEvent(self, event):
        pass

    def addCommandListeners(self, processor):
        self.__keyboard.addCommandListeners(processor)

    def removeCommandListeners(self, processor):
        self.__keyboard.removeCommandListeners(processor)

    def getCurrentForce(self):
        return self.__axisKeyBoard[FORCE_AXIS]

    def restart(self):
        ICMultiUpdate.restart(self)

    def _onSaveControls(self):
        self.__isSlipComp = InputMapping.g_instance.mouseSettings.SLIP_COMPENSATION
        BigWorld.player().cell.sendLiningFlag(clamp(0, self.__isSlipComp * 255, 255))
        settings = InputMapping.g_instance.mouseSettings
        camera = GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyNormal']
        cameraInertia = settings.INERTIA_CAMERA
        camera.speedRoll = CAMERA_ROLL_SPEED
        camera.speedYaw = CAMERA_YAW_SPEED + 2.0 * CAMERA_YAW_SPEED * (1.0 - cameraInertia) if cameraInertia > 0 else 100
        camera.speedPitch = CAMERA_PITCH_SPEED + 2.0 * CAMERA_PITCH_SPEED * (1.0 - cameraInertia) if cameraInertia > 0 else 100
        if InputMapping.g_instance.primarySettings.INVERT_VERT:
            self.__keyboard.verticalSign(1.0)
        else:
            self.__keyboard.verticalSign(-1.0)

    def slipCompensationVisualisation(self):
        if self.__isSlipComp and not self._notControlledByUser:
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
            hAxis = clamp(-1.0, self.__lastAxis[HORIZONTAL_AXIS] - (1.0 - abs(self.__lastAxis[HORIZONTAL_AXIS])) * clamp(-1.0, signX * angleX, 1.0), 1.0)
            owner.applyInputAxis(HORIZONTAL_AXIS, hAxis)
            vAxis = clamp(-1.0, self.__lastAxis[VERTICAL_AXIS] - (1.0 - abs(self.__lastAxis[VERTICAL_AXIS])) * clamp(-1.0, signY * angleY, 1.0), 1.0)
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