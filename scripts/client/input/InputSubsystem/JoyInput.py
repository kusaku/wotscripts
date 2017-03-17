# Embedded file name: scripts/client/input/InputSubsystem/JoyInput.py
import Keys
import BWPersonality
import InputMapping
import math
from MathExt import *
from consts import ROLL_AXIS, VERTICAL_AXIS, HORIZONTAL_AXIS, FORCE_AXIS, FLAPS_AXIS, INPUT_SYSTEM_STATE
from input.InputSubsystem.InputSubsystemBase import InputSubsystemBase
BASE_SMOOTH_WINDOW = 10

class JoystickExpertInput(InputSubsystemBase):

    def __init__(self, profile):
        self.__profile = profile
        self.__isRawForceAxis = True
        self.__smoothStack = {}
        self.__lastSmoothWin = {}

        class JoyEvent:

            def __init__(self):
                self.deviceId = None
                self.axis = None
                self.value = None
                return

        self.__joyEvent = JoyEvent()

    def pushLastEvent(self):
        for deviceId in BWPersonality.axis:
            for axis in BWPersonality.axis[deviceId]:
                self.__joyEvent.deviceId = deviceId
                self.__joyEvent.axis = axis
                self.__joyEvent.value = BWPersonality.axis[deviceId][axis]
                self.processJoystickEvent(self.__joyEvent)

    def restart(self):
        self.__smoothStack = {}
        self.__lastSmoothWin = {}

    def dispose(self):
        self.__profile = None
        return

    def processJoystickEvent(self, event):
        jSet = InputMapping.g_instance.joystickSettings
        if event.axis == jSet.ROLL_AXIS and (event.deviceId == jSet.ROLL_DEVICE or 0 == jSet.ROLL_DEVICE):
            rValue = -event.value if jSet.INVERT_ROLL else event.value
            rawValue = rValue
            if abs(rValue) <= jSet.ROLL_DEAD_ZONE:
                self.__profile.sendPrimaryAxis(ROLL_AXIS, 0.0, -rawValue)
            else:
                rValue = self.__signalSmoothing(jSet.ROLL_AXIS, rValue, jSet.ROLL_SMOOTH_WINDOW)
                rValue = self.__signalDiscrete(jSet.ROLL_SENSITIVITY, rValue, event.deviceId, event.axis)
                rValue = math.copysign((abs(rValue) - jSet.ROLL_DEAD_ZONE) / (1.0 - jSet.ROLL_DEAD_ZONE), rValue)
                rValue = InputMapping.translateAxisValue(jSet.AXIS_X_CURVE, rValue)
                self.__profile.sendPrimaryAxis(ROLL_AXIS, clamp(-1.0, -rValue, 1.0), -rawValue)
        elif event.axis == jSet.VERTICAL_AXIS and (event.deviceId == jSet.VERTICAL_DEVICE or 0 == jSet.VERTICAL_DEVICE):
            vValue = event.value if jSet.INVERT_VERTICAL else -event.value
            rawValue = vValue
            if abs(vValue) <= jSet.VERTICAL_DEAD_ZONE:
                self.__profile.sendPrimaryAxis(VERTICAL_AXIS, 0.0, rawValue)
            else:
                vValue = self.__signalSmoothing(jSet.VERTICAL_AXIS, vValue, jSet.VERTICAL_SMOOTH_WINDOW)
                vValue = self.__signalDiscrete(jSet.VERTICAL_SENSITIVITY, vValue, event.deviceId, event.axis)
                vValue = math.copysign((abs(vValue) - jSet.VERTICAL_DEAD_ZONE) / (1 - jSet.VERTICAL_DEAD_ZONE), vValue)
                vValue = InputMapping.translateAxisValue(jSet.AXIS_Y_CURVE, vValue)
                self.__profile.sendPrimaryAxis(VERTICAL_AXIS, clamp(-1.0, vValue, 1.0), rawValue)
        elif event.axis == jSet.HORIZONTAL_AXIS and (event.deviceId == jSet.HORIZONTAL_DEVICE or 0 == jSet.HORIZONTAL_DEVICE):
            hValue = event.value if jSet.INVERT_HORIZONTAL else -event.value
            rawValue = hValue
            if abs(hValue) <= jSet.HORIZONTAL_DEAD_ZONE:
                self.__profile.sendPrimaryAxis(HORIZONTAL_AXIS, 0.0, rawValue)
            else:
                hValue = self.__signalSmoothing(jSet.HORIZONTAL_AXIS, hValue, jSet.HORIZONTAL_SMOOTH_WINDOW)
                hValue = self.__signalDiscrete(jSet.HORIZONTAL_SENSITIVITY, hValue, event.deviceId, event.axis)
                hValue = InputMapping.translateAxisValue(jSet.AXIS_Z_CURVE, hValue)
                hValue = math.copysign((abs(hValue) - jSet.HORIZONTAL_DEAD_ZONE) / (1 - jSet.HORIZONTAL_DEAD_ZONE), hValue)
                if InputMapping.g_instance.currentProfileType == INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL:
                    hValue *= -1
                self.__profile.sendPrimaryAxis(HORIZONTAL_AXIS, clamp(-1.0, hValue, 1.0), rawValue)
        elif event.axis == jSet.FORCE_AXIS and (event.deviceId == jSet.FORCE_DEVICE or 0 == jSet.FORCE_DEVICE):
            fValue = -event.value if jSet.INVERT_FORCE else event.value
            rawValue = fValue
            if self.__isRawForceAxis:
                fValue = self.__renormalization(fValue)
            self.__profile.sendPrimaryAxis(FORCE_AXIS, fValue, rawValue)

    def setCursorCamera(self, isCursorCamera):
        pass

    def setRawForceAxis(self, value):
        self.__isRawForceAxis = value

    def __renormalization(self, x):
        maxForce = InputMapping.g_instance.joystickSettings.POINT_OF_NORMAL_THRUST
        deadZone = InputMapping.g_instance.joystickSettings.FORCE_DEAD_ZONE
        if deadZone > 1:
            deadZone = 1
        if x > deadZone:
            return 1
        if maxForce < x <= deadZone:
            return 0
        return clamp(-1.0, (x + 1.0) / (max(-0.99, maxForce) + 1.0) - 1.0, 0.0)

    def __signalDiscrete(self, discrete, value, deviceId, axis):
        SENSITIVITY = 14 * discrete
        joyDPI = BigWorld.getJoystickResolution(deviceId, axis) / pow(2.0, math.floor(SENSITIVITY))
        halfSingleSignal = 0.5 / joyDPI
        if abs(value) < 0.25 * halfSingleSignal or abs(value) > 1.0 - 0.25 * halfSingleSignal:
            return value
        absValue = math.floor(abs(value) * joyDPI) / joyDPI + halfSingleSignal
        return math.copysign(absValue, value)

    def __signalSmoothing(self, axis, value, win, e = 0.99):
        if self.__lastSmoothWin.get(axis, None) != win:
            self.__lastSmoothWin[axis] = win
            if self.__smoothStack.get(axis, None):
                self.__smoothStack[axis] = []
        window = max(int(BASE_SMOOTH_WINDOW * win), 1)
        self.__smoothStack.setdefault(axis, []).append(value)
        if len(self.__smoothStack[axis]) > window:
            self.__smoothStack[axis].pop(0)
        val = math.copysign(1.0, value) if abs(value) >= e else sum(self.__smoothStack[axis]) / len(self.__smoothStack[axis])
        return val