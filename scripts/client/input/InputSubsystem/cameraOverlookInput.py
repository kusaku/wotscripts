# Embedded file name: scripts/client/input/InputSubsystem/cameraOverlookInput.py
__author__ = 'm_kobets'
import math
import Math
import BigWorld
import InputMapping
import GameEnvironment
from MathExt import clamp
from ICMultiUpdate import ICMultiUpdate
from consts import FREE_HORIZONTAL_CAM_GAMEPAD, FREE_VERTICAL_CAM_GAMEPAD

class SIDE:
    FRONT = Math.Vector3(1, 0, 0)
    BACK = Math.Vector3(-1, 0, 0)
    RIGHT = Math.Vector3(0, 1, 0)
    LEFT = Math.Vector3(0, -1, 0)
    UP = Math.Vector3(0, 0, 1)
    DOWN = Math.Vector3(0, 0, -1)


_SENSITIVITY_CFC = 0.1
_BASE_SMOOTH_WINDOW = 10
_HUD_MANAGER_UPDATE_TIME = 0.1

class cameraOverlookInput(ICMultiUpdate):

    def __init__(self):
        self.__keyMainDirect = Math.Vector3(0, 0, 0)
        self.__keyStaticDirect = Math.Vector3(0, 0, 0)
        self.__axisValue = {FREE_HORIZONTAL_CAM_GAMEPAD: 0,
         FREE_VERTICAL_CAM_GAMEPAD: 0}
        self.__mouseExtraValue = {'x': 0,
         'y': 0}
        self.__mapping_function = {}
        self.__mouseMode = False
        self.__turnSpeed = 100
        self.__staticVision = False
        self.__lastSmoothWin = {}
        self.__smoothStack = {}
        self.__enemyTarget = None
        self.__linkEvents()
        self.__cameraStrategy.resetOwerLook()
        self.__last_hud_switch = False
        ICMultiUpdate.__init__(self, (_HUD_MANAGER_UPDATE_TIME, self.__hudManager))
        return

    def __linkEvents(self):
        GameEnvironment.getHUD().eSetTargetEntity += self.__setEnemyTarget

    def __unlinkEvents(self):
        GameEnvironment.getHUD().eSetTargetEntity -= self.__setEnemyTarget

    @property
    def __cameraStrategy(self):
        return GameEnvironment.getCamera().getDefualtStrategies['CameraStrategyNormal']

    def __hudManager(self):
        active = self.__cameraStrategy.action
        if active != self.__last_hud_switch:
            self.__last_hud_switch = active
            GameEnvironment.getHUD().setTargetVisible(not active)

    def __setEnemyTarget(self, enemy):
        if self.__enemyTarget != enemy and enemy is not None:
            self.__enemyTarget = enemy
            self.__cameraStrategy.enemyTargetMatrix = enemy.matrix
        return

    def restart(self):
        self.__lastSmoothWin = {}
        self.__smoothStack = {}
        self.__last_hud_activity = False
        ICMultiUpdate.restart(self)

    def dispose(self):
        self.__freeOutAllButtonsOnDestroy()
        ICMultiUpdate.dispose(self)
        self.__mapping_function = {}
        self.__enemyTarget = None
        self.__unlinkEvents()
        return

    def setFlexibility(self, value):
        self.__cameraStrategy.flexibility = value

    def setTurnSpeed(self, value):
        self.__turnSpeed = value

    def setToMainVision(self):
        self.__cameraStrategy.resetCameraRotation()

    def __enableTargetLook(self, fired):
        on_of = fired and self.__enemyTarget is not None
        self.__cameraStrategy.enableTargetLook(on_of)
        return

    def __cmdKeyTurn(self, fired, turnDir):
        self.__keyMainDirect += turnDir if fired else -1 * turnDir
        if fired:
            self.__keyStaticDirect = turnDir
        direction = self.__keyStaticDirect if self.__staticVision else self.__keyMainDirect
        self.__cameraStrategy.keyInput(direction.x, direction.y, direction.z)

    def processJoystickEvent(self, event):
        jSet = InputMapping.g_instance.joystickSettings
        if event.axis == jSet.FREE_HORIZONTAL_CAM_GAMEPAD_AXIS and (event.deviceId == jSet.FREE_HORIZONTAL_CAM_GAMEPAD_DEVICE or 0 == jSet.FREE_HORIZONTAL_CAM_GAMEPAD_DEVICE):
            hValue = event.value
            if abs(hValue) <= jSet.FREE_HORIZONTAL_CAM_GAMEPAD_DEAD_ZONE:
                hValue = 0.0
            else:
                hValue = math.copysign((abs(hValue) - jSet.FREE_HORIZONTAL_CAM_GAMEPAD_DEAD_ZONE) / (1 - jSet.FREE_HORIZONTAL_CAM_GAMEPAD_DEAD_ZONE), hValue)
            hValue = self.__signalSmoothing(jSet.FREE_HORIZONTAL_CAM_GAMEPAD_AXIS, hValue, jSet.FREE_HORIZONTAL_CAM_GAMEPAD_SMOOTH_WINDOW)
            hValue = self.__signalDiscrete(jSet.FREE_HORIZONTAL_CAM_GAMEPAD_SENSITIVITY, hValue, event.deviceId, event.axis)
            self.__axisValue[FREE_HORIZONTAL_CAM_GAMEPAD] = clamp(-1.0, hValue, 1.0)
            self.__setAxisMove()
        elif event.axis == jSet.FREE_VERTICAL_CAM_GAMEPAD_AXIS and (event.deviceId == jSet.FREE_VERTICAL_CAM_GAMEPAD_DEVICE or 0 == jSet.FREE_VERTICAL_CAM_GAMEPAD_DEVICE):
            vValue = event.value
            if abs(vValue) <= jSet.FREE_VERTICAL_CAM_GAMEPAD_DEAD_ZONE:
                vValue = 0.0
            else:
                vValue = math.copysign((abs(vValue) - jSet.FREE_VERTICAL_CAM_GAMEPAD_DEAD_ZONE) / (1 - jSet.FREE_VERTICAL_CAM_GAMEPAD_DEAD_ZONE), vValue)
            vValue = self.__signalSmoothing(jSet.FREE_VERTICAL_CAM_GAMEPAD_AXIS, vValue, jSet.FREE_VERTICAL_CAM_GAMEPAD_SMOOTH_WINDOW)
            vValue = self.__signalDiscrete(jSet.FREE_VERTICAL_CAM_GAMEPAD_SENSITIVITY, vValue, event.deviceId, event.axis)
            vValue = vValue if jSet.INVERT_FREE_VERTICAL_CAM_GAMEPAD else -vValue
            self.__axisValue[FREE_VERTICAL_CAM_GAMEPAD] = clamp(-1.0, vValue, 1.0)
            self.__setAxisMove()

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
        if value != 0:
            window = max(int(_BASE_SMOOTH_WINDOW * win), 1)
            self.__smoothStack.setdefault(axis, []).append(value)
            if len(self.__smoothStack[axis]) > window:
                self.__smoothStack[axis].pop(0)
            if abs(value) >= e:
                return math.copysign(1.0, value)
            return sum(self.__smoothStack[axis]) / len(self.__smoothStack[axis])
        else:
            self.__smoothStack[axis] = [0]
            return 0
            return

    def __setAxisMove(self):
        x = self.__axisValue[FREE_HORIZONTAL_CAM_GAMEPAD]
        y = self.__axisValue[FREE_VERTICAL_CAM_GAMEPAD]
        self.__cameraStrategy.axisInput(-y, x)

    def processMouseEvent(self, event):
        """ main mouse event """
        y = math.radians(_SENSITIVITY_CFC * event.dy)
        x = math.radians(_SENSITIVITY_CFC * event.dx)
        self.__cameraStrategy.mouseInput(y, x)

    def __activateMouse(self, value):
        self.__mouseMode = bool(value)
        self.__cameraStrategy.activeMouseMove(self.__mouseMode)
        self.__mixInput(None, None)
        return

    def __setStaticVision(self, value):
        self.__staticVision = value
        if not self.__keyMainDirect.length:
            self.__keyStaticDirect = Math.Vector3(0, 0, 0)
        self.__mixInput(None, None)
        return

    def __extraMouseMoveX(self, dx):
        self.__mouseExtraValue['x'] = math.radians(self.__turnSpeed * dx)
        self.__cameraStrategy.mouseExtraInput(self.__mouseExtraValue['y'], self.__mouseExtraValue['x'])

    def __extraMouseMoveY(self, dy):
        self.__mouseExtraValue['y'] = math.radians(-self.__turnSpeed * dy)
        self.__cameraStrategy.mouseExtraInput(self.__mouseExtraValue['y'], self.__mouseExtraValue['x'])

    def __mixInput(self, fired, turnDir):
        if turnDir == SIDE.LEFT or turnDir == SIDE.RIGHT:
            self.__mouseExtraValue['x'] = math.radians(self.__turnSpeed * turnDir.y * fired)
        elif turnDir == SIDE.FRONT or turnDir == SIDE.BACK:
            self.__mouseExtraValue['y'] = math.radians(-self.__turnSpeed * turnDir.x * fired)
        elif turnDir == SIDE.LEFT + SIDE.FRONT or turnDir == SIDE.RIGHT + SIDE.BACK:
            sign = 1 if turnDir == SIDE.LEFT + SIDE.FRONT else -1
            self.__mouseExtraValue['x'] = math.radians(self.__turnSpeed * -sign * fired)
            self.__mouseExtraValue['y'] = math.radians(-self.__turnSpeed * sign * fired)
        elif turnDir == SIDE.RIGHT + SIDE.FRONT or turnDir == SIDE.LEFT + SIDE.BACK:
            sign = 1 if turnDir == SIDE.RIGHT + SIDE.FRONT else -1
            self.__mouseExtraValue['x'] = math.radians(self.__turnSpeed * sign * fired)
            self.__mouseExtraValue['y'] = math.radians(-self.__turnSpeed * sign * fired)
        if fired is not None and turnDir is not None:
            self.__keyMainDirect += turnDir if fired else -1 * turnDir
            if fired:
                self.__keyStaticDirect = turnDir
        if self.__mouseMode:
            self.__cameraStrategy.mouseExtraInput(self.__mouseExtraValue['y'], self.__mouseExtraValue['x'])
        else:
            direction = self.__keyStaticDirect if self.__staticVision else self.__keyMainDirect
            self.__cameraStrategy.keyInput(direction.x, direction.y, direction.z)
        return

    def __addCMD(self, processor, cmd, side):
        func = lambda value: self.__mixInput(value, side)
        processor.addListeners(cmd, None, None, func)
        self.__mapping_function[cmd] = func
        return

    def addCommandListeners(self, processor):
        processor.addListeners(InputMapping.CMD_OVERLOOK_MOD, None, None, self.__activateMouse)
        processor.addListeners(InputMapping.CMD_STATIC_MOD, None, None, self.__setStaticVision)
        processor.addListeners(InputMapping.CMD_TARGET_CAMERA, None, None, self.__enableTargetLook)
        CMD_DICT = {InputMapping.CMD_SIDE_VIEW_LEFT: SIDE.LEFT,
         InputMapping.CMD_SIDE_VIEW_RIGHT: SIDE.RIGHT,
         InputMapping.CMD_FRONT_VIEW: SIDE.FRONT,
         InputMapping.CMD_BACK_VIEW: SIDE.BACK,
         InputMapping.CMD_SIDE_VIEW_UP_LEFT: SIDE.LEFT + SIDE.FRONT,
         InputMapping.CMD_SIDE_VIEW_UP_RIGHT: SIDE.RIGHT + SIDE.FRONT,
         InputMapping.CMD_SIDE_VIEW_DOWN_LEFT: SIDE.LEFT + SIDE.BACK,
         InputMapping.CMD_SIDE_VIEW_DOWN_RIGHT: SIDE.RIGHT + SIDE.BACK,
         InputMapping.CMD_SIDE_VIEW_UP: SIDE.UP,
         InputMapping.CMD_SIDE_VIEW_DOWN: SIDE.DOWN}
        for cmd, side in CMD_DICT.iteritems():
            self.__addCMD(processor, cmd, side)

        return

    def removeCommandListeners(self, processor):
        processor.removeListeners(InputMapping.CMD_OVERLOOK_MOD, None, None, self.__activateMouse)
        processor.removeListeners(InputMapping.CMD_STATIC_MOD, None, None, self.__setStaticVision)
        processor.removeListeners(InputMapping.CMD_TARGET_CAMERA, None, None, self.__enableTargetLook)
        CMD_LIST = [InputMapping.CMD_SIDE_VIEW_LEFT,
         InputMapping.CMD_SIDE_VIEW_RIGHT,
         InputMapping.CMD_FRONT_VIEW,
         InputMapping.CMD_BACK_VIEW,
         InputMapping.CMD_SIDE_VIEW_UP_LEFT,
         InputMapping.CMD_SIDE_VIEW_UP_RIGHT,
         InputMapping.CMD_SIDE_VIEW_DOWN_LEFT,
         InputMapping.CMD_SIDE_VIEW_DOWN_RIGHT,
         InputMapping.CMD_SIDE_VIEW_UP,
         InputMapping.CMD_SIDE_VIEW_DOWN]
        for cmd in CMD_LIST:
            processor.removeListeners(cmd, None, None, self.__mapping_function[cmd])

        return

    def __freeOutAllButtonsOnDestroy(self):
        """
            some chit. Need on switch InputSystem.
        """
        buttons_cmd_list = [InputMapping.CMD_OVERLOOK_MOD,
         InputMapping.CMD_STATIC_MOD,
         InputMapping.CMD_TARGET_CAMERA,
         InputMapping.CMD_SIDE_VIEW_LEFT,
         InputMapping.CMD_SIDE_VIEW_RIGHT,
         InputMapping.CMD_FRONT_VIEW,
         InputMapping.CMD_BACK_VIEW,
         InputMapping.CMD_SIDE_VIEW_UP_LEFT,
         InputMapping.CMD_SIDE_VIEW_UP_RIGHT,
         InputMapping.CMD_SIDE_VIEW_DOWN_LEFT,
         InputMapping.CMD_SIDE_VIEW_DOWN_RIGHT,
         InputMapping.CMD_SIDE_VIEW_UP,
         InputMapping.CMD_SIDE_VIEW_DOWN]
        commandProcessor = GameEnvironment.getInput().commandProcessor
        for cmd in buttons_cmd_list:
            commandProcessor.getCommand(cmd).isFired = False