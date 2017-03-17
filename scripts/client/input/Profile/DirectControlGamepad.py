# Embedded file name: scripts/client/input/Profile/DirectControlGamepad.py
import BigWorld
import GameEnvironment
from ICMultiUpdate import ICMultiUpdate
import InputMapping
from MathExt import clamp, FloatToCInt16
import math
from _preparedBattleData_db import preparedBattleData
from consts import FORCE_AXIS, FLAPS_AXIS, ROLL_AXIS, VERTICAL_AXIS, HORIZONTAL_AXIS
from input.InputSubsystem.GamepadInput import GamepadInput
from input.InputSubsystem.KeyboardInput import KeyboardInput
from input.Profile.ProfileBase import IProfileBase

class DirectControlGamepad(IProfileBase, ICMultiUpdate):

    def __init__(self, inputAxis, notControlledByUser):
        self._notControlledByUser = notControlledByUser
        self._forciblySendAxis = False
        InputMapping.g_instance.onSaveControls += self._onSaveControls
        ICMultiFunction = lambda : (self.__autopilotUpdate() if self._notControlledByUser else None)
        ICMultiUpdate.__init__(self, (0.1, ICMultiFunction))
        self.__axisKeyBoard = [0.0] * 5
        self.__axisJoy = [0.0] * 5
        self.__lastAxis = [0.0] * 5
        self.__gamepad = GamepadInput(self)
        self.__keyboard = KeyboardInput(self)
        self._onSaveControls()

    def getCurrentForce(self):
        return self.__axisJoy[FORCE_AXIS]

    def dispose(self):
        InputMapping.g_instance.onSaveControls -= self._onSaveControls
        self.__gamepad.dispose()
        self.__keyboard.dispose()
        self.__gamepad = None
        self.__keyboard = None
        return

    def restart(self):
        pass

    def _onSaveControls(self):
        pass

    def setCamDirection(self, direction):
        pass

    def __send(self, axis):
        player = BigWorld.player()
        value = self.__axisJoy[axis] * (1.0 - abs(self.__axisKeyBoard[axis])) + self.__axisKeyBoard[axis]
        if self.__lastAxis[axis] != value:
            player.cell.sendInputJoyAxis(axis, FloatToCInt16(value))
            player.applyInputAxis(axis, value)
            self.__lastAxis[axis] = value

    def sendAxis(self, axis, value):
        self.__axisKeyBoard[axis] = value
        if self._notControlledByUser:
            return
        self.__send(axis)

    def sendPrimaryAxis(self, axis, value):
        self.__axisJoy[axis] = value
        if self._notControlledByUser:
            return
        self.__send(axis)

    def notControlledByUser(self, value):
        self._notControlledByUser = value
        self.__gamepad.notControlledByUser(value)
        if not self._notControlledByUser:
            for axis in range(0, 5):
                self.__send(axis)

    def processMouseEvent(self, event):
        pass

    def processJoystickEvent(self, event):
        self.__gamepad.processJoystickEvent(event)

    def addCommandListeners(self, processor):
        self.__keyboard.addCommandListeners(processor)

    def removeCommandListeners(self, processor):
        self.__keyboard.removeCommandListeners(processor)

    def __autopilotUpdate(self):
        """successor should provide an update of this method through its own ICMultiUpdate """
        owner = BigWorld.player()
        if abs(owner.pitch) < 0.25 * math.pi:
            rollAxis = owner.roll * 0.5
            rollAxis = min(1.0, max(-1.0, rollAxis))
            owner.applyInputAxis(ROLL_AXIS, -rollAxis)
        pitchAxis = owner.pitch
        pitchAxis = min(1.0, max(-1.0, pitchAxis))
        owner.applyInputAxis(VERTICAL_AXIS, pitchAxis)
        owner.applyInputAxis(HORIZONTAL_AXIS, 0)