# Embedded file name: scripts/client/input/InputSubsystem/KeyboardInput.py
import InputMapping
from MathExt import *
from EntityHelpers import EntityStates
from consts import FORCE_AXIS, ROLL_AXIS, VERTICAL_AXIS, HORIZONTAL_AXIS, FLAPS_AXIS, SERVER_TICK_LENGTH, DEFAULT_LATENCY
from input.InputSubsystem.InputSubsystemBase import *
from ICMultiUpdate import ICMultiUpdate
MAX_AXIS_TIME = 1.0
MIN_AXIS_TIME = 0.0

class KeyboardInput(InputSubsystemBase, ICMultiUpdate):

    def __init__(self, profile):
        self.__profile = profile
        self.__axis = [0] * 5
        self.__targetForce = 0
        self.__incForce = False
        self.__decForce = False
        self.__verticalSign = 1.0
        self.__isMultiplySignal = True
        ICMultiUpdate.__init__(self, (0.1, self.__slipCompensationVisualisation))
        self.restart()

    def __slipCompensationVisualisation(self):
        self.__profile.slipCompensationVisualisation()

    def dispose(self):
        for axis in self.__QueueAxesSend:
            if axis.timerCallBack is not None:
                BigWorld.cancelCallback(axis.timerCallBack)

        self.__profile = None
        self.__axis = None
        ICMultiUpdate.dispose(self)
        return

    def restart(self):
        ICMultiUpdate.restart(self)
        self.__QueueAxesSend = [SendQueueElementAxes(), SendQueueElementAxes(), SendQueueElementAxes()]

    @property
    def isMultiplySignal(self):
        return self.__isMultiplySignal

    @isMultiplySignal.setter
    def isMultiplySignal(self, value):
        self.__isMultiplySignal = value

    def addCommandListeners(self, processor):
        processor.addListeners(InputMapping.CMD_TURN_LEFT, None, None, self.__cmdTurnLeft)
        processor.addListeners(InputMapping.CMD_TURN_RIGHT, None, None, self.__cmdTurnRight)
        processor.addListeners(InputMapping.CMD_PITCH_DOWN, None, None, self.__cmdPitchDown)
        processor.addListeners(InputMapping.CMD_PITCH_UP, None, None, self.__cmdPitchUp)
        processor.addListeners(InputMapping.CMD_ROLL_LEFT, None, None, self.__cmdRollLeft)
        processor.addListeners(InputMapping.CMD_ROLL_RIGHT, None, None, self.__cmdRollRight)
        processor.addListeners(InputMapping.CMD_INCREASE_FORCE, None, None, self.__cmdIncForce)
        processor.addListeners(InputMapping.CMD_DECREASE_FORCE, None, None, self.__cmdDecForce)
        processor.addListeners(InputMapping.CMD_FLAPS_UP, None, None, self.__cmdSetFlapsState)
        processor.addListeners(InputMapping.CMD_ENGINE_OFF, None, None, self.__cmdEngineOff)
        processor.addListeners(InputMapping.CMD_INC_TARGET_FORCE, self.__cmdIncTargetForceStart, self.__cmdIncTargetForceEnd)
        processor.addListeners(InputMapping.CMD_DEC_TARGET_FORCE, self.__cmdDecTargetForce)
        return

    def removeCommandListeners(self, processor):
        processor.removeListeners(InputMapping.CMD_TURN_LEFT, None, None, self.__cmdTurnLeft)
        processor.removeListeners(InputMapping.CMD_TURN_RIGHT, None, None, self.__cmdTurnRight)
        processor.removeListeners(InputMapping.CMD_PITCH_DOWN, None, None, self.__cmdPitchDown)
        processor.removeListeners(InputMapping.CMD_PITCH_UP, None, None, self.__cmdPitchUp)
        processor.removeListeners(InputMapping.CMD_ROLL_LEFT, None, None, self.__cmdRollLeft)
        processor.removeListeners(InputMapping.CMD_ROLL_RIGHT, None, None, self.__cmdRollRight)
        processor.removeListeners(InputMapping.CMD_INCREASE_FORCE, None, None, self.__cmdIncForce)
        processor.removeListeners(InputMapping.CMD_DECREASE_FORCE, None, None, self.__cmdDecForce)
        processor.removeListeners(InputMapping.CMD_FLAPS_UP, None, None, self.__cmdSetFlapsState)
        processor.removeListeners(InputMapping.CMD_ENGINE_OFF, None, None, self.__cmdEngineOff)
        processor.removeListeners(InputMapping.CMD_INC_TARGET_FORCE, self.__cmdIncTargetForceStart, self.__cmdIncTargetForceEnd)
        processor.removeListeners(InputMapping.CMD_DEC_TARGET_FORCE, self.__cmdDecTargetForce)
        return

    def verticalSign(self, value):
        self.__verticalSign = value

    def __cmdTurnRight(self, fired):
        if fired:
            self.__axis[HORIZONTAL_AXIS] += 1
        else:
            self.__axis[HORIZONTAL_AXIS] -= 1
        self.onInputAxisChange(HORIZONTAL_AXIS, self.__axis[HORIZONTAL_AXIS])

    def __cmdTurnLeft(self, fired):
        if fired:
            self.__axis[HORIZONTAL_AXIS] -= 1
        else:
            self.__axis[HORIZONTAL_AXIS] += 1
        self.onInputAxisChange(HORIZONTAL_AXIS, self.__axis[HORIZONTAL_AXIS])

    def __cmdPitchDown(self, fired):
        if fired:
            self.__axis[VERTICAL_AXIS] -= self.__verticalSign
        else:
            self.__axis[VERTICAL_AXIS] += self.__verticalSign
        self.onInputAxisChange(VERTICAL_AXIS, self.__axis[VERTICAL_AXIS])

    def __cmdPitchUp(self, fired):
        if fired:
            self.__axis[VERTICAL_AXIS] += self.__verticalSign
        else:
            self.__axis[VERTICAL_AXIS] -= self.__verticalSign
        self.onInputAxisChange(VERTICAL_AXIS, self.__axis[VERTICAL_AXIS])

    def __cmdRollRight(self, fired):
        if fired:
            self.__axis[ROLL_AXIS] -= 1
        else:
            self.__axis[ROLL_AXIS] += 1
        self.onInputAxisChange(ROLL_AXIS, self.__axis[ROLL_AXIS])

    def __cmdRollLeft(self, fired):
        if fired:
            self.__axis[ROLL_AXIS] += 1
        else:
            self.__axis[ROLL_AXIS] -= 1
        self.onInputAxisChange(ROLL_AXIS, self.__axis[ROLL_AXIS])

    def __axisTimeCfc(self, time, sensetive):
        axisTime = MIN_AXIS_TIME + MAX_AXIS_TIME * (1.0 - sensetive)
        if axisTime > 0.0:
            return clamp(0.0, time / axisTime, 1.0)
        else:
            return 1.0

    def __sendForce(self):
        force = clamp(-1.0, self.__targetForce + (self.__incForce - self.__decForce), 1.0)
        self.__axis[FORCE_AXIS] = 1.0 if force > 0 else force
        self.__profile.sendAxis(FORCE_AXIS, self.__axis[FORCE_AXIS])

    def getCurrentForce(self):
        return self.__axis[FORCE_AXIS]

    def __cmdIncTargetForceStart(self):
        if not self.__incForce:
            if self.__targetForce == 0:
                self.__targetForce = 1
            else:
                self.__targetForce = min(self.__targetForce + 0.2, 0)
            self.__sendForce()

    def __cmdIncTargetForceEnd(self):
        if self.__targetForce == 1:
            self.__targetForce = 0
            self.__sendForce()

    def __cmdDecTargetForce(self):
        if not self.__incForce:
            self.__targetForce = max(self.__targetForce - 0.2, -1)
            self.__sendForce()

    def __cmdIncForce(self, incForce):
        self.__incForce = incForce
        self.__sendForce()

    def __cmdDecForce(self, decForce):
        self.__decForce = decForce
        self.__sendForce()

    def __cmdEngineOff(self, isOff):
        self.__decForce = isOff
        self.__sendForce()

    def __cmdSetFlapsState(self, isUp):
        self.__profile.sendAxis(FLAPS_AXIS, int(isUp))

    def onInputAxisChange(self, axis, value):
        """send input axis to server"""
        if not self.__isMultiplySignal:
            self.__profile.sendAxis(axis, clamp(-1.0, value, 1.0))
            return
        else:
            time = BigWorld.time()
            dt = time - self.__QueueAxesSend[axis].lastDispatch
            if dt < SERVER_TICK_LENGTH:
                self.__QueueAxesSend[axis].listToSend.append((time, value))
                if self.__QueueAxesSend[axis].timerCallBack == None:
                    func = lambda : self.__sendingInputQueue(axis, time)
                    self.__QueueAxesSend[axis].timerCallBack = BigWorld.callback(SERVER_TICK_LENGTH - dt, func)
            else:
                self.__QueueAxesSend[axis].listToSend.append((time, value))
                self.__sendingInputQueue(axis, time)
            return

    def __sendingInputQueue(self, axis, time):
        if self.__QueueAxesSend[axis].timerCallBack != None:
            BigWorld.cancelCallback(self.__QueueAxesSend[axis].timerCallBack)
            self.__QueueAxesSend[axis].timerCallBack = None
        if len(self.__QueueAxesSend[axis].listToSend) != 1:
            value, lastValue = self.__getInputQueueValue(axis, time)
        else:
            value = self.__QueueAxesSend[axis].listToSend[0][1]
            lastValue = value
        func = lambda : self.__sendingInputQueue(axis, BigWorld.time())
        self.__QueueAxesSend[axis].timerCallBack = BigWorld.callback(SERVER_TICK_LENGTH, func)
        self.__profile.sendAxis(axis, clamp(-1.0, value, 1.0))
        self.__QueueAxesSend[axis].lastDispatch = time
        self.__QueueAxesSend[axis].listToSend = [(time, lastValue)]
        return

    def __getInputQueueValue(self, axis, time):
        lastDispatch = self.__QueueAxesSend[axis].lastDispatch
        result = 0.0
        time1 = max(0, self.__QueueAxesSend[axis].listToSend[0][0] - lastDispatch)
        h = self.__QueueAxesSend[axis].listToSend[0][1]
        for index in range(1, len(self.__QueueAxesSend[axis].listToSend)):
            time2 = self.__QueueAxesSend[axis].listToSend[index][0] - lastDispatch
            dt = time2 - time1
            result += h * dt / SERVER_TICK_LENGTH
            time1 = time2
            h = self.__QueueAxesSend[axis].listToSend[index][1]

        dt = time - lastDispatch - time1
        result += h * dt / SERVER_TICK_LENGTH
        return (result, h)


class SendQueueElementAxes:

    def __init__(self):
        self.lastDispatch = 0.0
        self.timerCallBack = None
        self.listToSend = [(0.0, 0.0)]
        return