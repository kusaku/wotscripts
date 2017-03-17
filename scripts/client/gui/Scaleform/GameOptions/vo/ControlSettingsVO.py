# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/ControlSettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import ArrayIndex
from gui.Scaleform.GameOptions.utils import Point
from gui.Scaleform.GameOptions.utils import JOYSTICK_PRESETS_KEYS
from gui.Scaleform.GameOptions.utils import GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS
from gui.Scaleform.GameOptions.utils import MOUSE_PRESETS_KEYS

class ButtonEntryVO:

    def __init__(self):
        self.isLazy = False
        self.id = ''
        self.label = ''
        self.deviceId = ''


class AxisEntryVO:

    def __init__(self):
        self.isLazy = False
        self.axisId = -1
        self.axisInverted = False
        self.axisSensitivity = 0.0
        self.axisDeadzone = 0.0
        self.axisDeviceId = ''
        self.axisDeviceName = ''
        self.axisLabel = ''
        self.isFireAxis = False
        self.sign = 0
        self.axisGroup = ''
        self.axisSmoothing = 0.0


class CommandVO:

    def __init__(self):
        self.isLazy = False
        self.id = 0
        self.title = ''
        self.buttons = list()
        self.switchingStyle = 0
        self.enabled = True
        self.axes = AxisEntryVO()


class GroupControlVO:

    def __init__(self):
        self.isLazy = True
        self.id = -1
        self.title = ''
        self.controls = list()


class MousePresetVO:

    def __init__(self):
        self.isLazy = True
        self.allowLead = 0
        self.cameraType = 0
        self.mouseInvertVert = False
        self.safeRollOnLowAltitude = False
        self.automaticFlaps = False
        self.tighteningLeft = Point()
        self.tighteningLeftTop = Point()
        self.tighteningCenter = Point()
        self.tighteningRightBottom = Point()
        self.tighteningRight = Point()
        self.supermouseCameraFlexibility = 0.0
        self.radiusOfConducting = 0.0
        self.supermouseEqualizerForce = 0.0
        self.supermouseEqualizerZoneSize = 0.0
        self.supermouseRollSpeed = 0.0
        self.supermouseRotationZoneDepth = True
        self.cameraAcceleration = 0.0
        self.cameraRollSpeed = 0.0
        self.cameraAngle = 0.0
        self.methodOfMixing = ArrayIndex()


class MouseProfileVO:

    def __init__(self):
        self.isLazy = True
        self.customPresetName = 'mouseCustomPreset'
        self.mouseSensitivity = 0.0
        self.profilePreset = ArrayIndex()
        self.groupControls = list()
        for presetFlashKey in MOUSE_PRESETS_KEYS.iterkeys():
            setattr(self, presetFlashKey, MousePresetVO())


class GamepadPresetVO:

    def __init__(self):
        self.isLazy = True
        self.id = -1
        self.groupControls = list()
        self.allCurves = list()
        self.maxForce = 0.0
        self.allowLead = 0
        self.cameraType = 0
        self.commonAxisInverted = False
        self.commonAxisDeadzone = 0.0
        self.safeRollOnLowAltitude = False
        self.automaticFlaps = False
        self.supermouseCameraFlexibility = 0.0
        self.radiusOfConducting = 0.0
        self.supermouseEqualizerForce = 0.0
        self.supermouseEqualizerZoneSize = 0.0
        self.supermouseRollSpeed = 0.0
        self.supermouseRotationZoneDepth = True
        self.cameraAcceleration = 0.0
        self.cameraRollSpeed = 0.0
        self.cameraAngle = 0.0
        self.sensitivity = 0.0


class GamepadProfileVO:

    def __init__(self):
        self.isLazy = True
        self.id = -1
        self.profilePreset = ArrayIndex()
        self.customPresetName = 'gamepad_direct_control'
        for presetFlashKey in GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS.iterkeys():
            setattr(self, presetFlashKey, GamepadPresetVO())


class JoystickPresetVO:

    def __init__(self):
        self.isLazy = True
        self.id = -1
        self.groupControls = list()
        self.maxForce = 0.0
        self.verticalCurve = list()
        self.horisontalCurve = list()
        self.rollCurve = list()
        self.inertiaCamera = 1.0
        self.slipCompensationValue = 1.0
        self.hutSpeed = 1.0
        self.inertiaCameraRoll = 1.0
        self.sensitivityInSniperMode = 1.0


class JoystickProfileVO:

    def __init__(self):
        self.isLazy = True
        self.id = -1
        self.profilePreset = ArrayIndex()
        self.customPresetName = 'joystick'
        for presetFlashKey in JOYSTICK_PRESETS_KEYS.iterkeys():
            setattr(self, presetFlashKey, JoystickPresetVO())


class KeyboardProfileVO:

    def __init__(self):
        self.isLazy = True
        self.slipCompensation = False
        self.keyboardInvertVert = True
        self.groupControls = list()
        self.inertiaCamera = 1.0


class ControlConstantsVO:

    def __init__(self):
        self.isLazy = False
        self.forceCmd = -1
        self.turnCmd = -1
        self.pitchCmd = -1
        self.rollCmd = -1
        self.cmdFreeVerticalCam = -1
        self.cmdFreeHorizontalCam = -1
        self.cmdFreeVerticalCamDesc = ''
        self.cmdFreeHorizontalCamDesc = ''
        self.rollCmdDesc = ''
        self.pitchCmdDesc = ''
        self.turnCmdDesc = ''
        self.forceCmdDesc = ''
        self.turnGamepadCmd = -1
        self.pitchGamepadCmd = -1
        self.rollGamepadCmd = -1
        self.forceGamepadCmd = -1
        self.freeVerticalCamGamepadCmd = -1
        self.freeHorizontalCamGamepadCmd = -1
        self.inputHorizontalAxisId = -1
        self.inputVerticalAxisId = -1
        self.inputRollAxisId = -1
        self.inputForceAxisId = -1
        self.inputFlapsAxisId = -1
        self.inputFreeVerticalCamGamepadAxisId = -1
        self.inputFreeHorizontalCamGamepadAxisId = -1


class ControlSettingsVO:

    def __init__(self):
        self.isLazy = False
        self.controlConstants = ControlConstantsVO()
        self.controlProfiles = ArrayIndex()
        self.fastFM = False
        self.profileMouse051 = MouseProfileVO()
        self.profileGamepadDirectControl = GamepadProfileVO()
        self.profileJoystick = JoystickProfileVO()
        self.profileKeyboard = KeyboardProfileVO()