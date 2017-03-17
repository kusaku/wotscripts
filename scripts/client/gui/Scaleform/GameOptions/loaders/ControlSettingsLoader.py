# Embedded file name: scripts/client/gui/Scaleform/GameOptions/loaders/ControlSettingsLoader.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BaseLoader, isTutorial
from gui.Scaleform.GameOptions.utils import ORDER_PROFILES
from gui.Scaleform.GameOptions.utils import KeyValue
from gui.Scaleform.GameOptions.utils import ALL_PRESETS_KEYS_REVERT, ALL_PRESETS_KEYS, GAMEPAD_DIRECT_DATA_CURVE
from gui.Scaleform.GameOptions.utils import MOUSE_TIGHTENING_KEYS, MOUSE_INTENSITY_SPLINE_KEY, JOYSTICK_DATA_CURVE
from Helpers.i18n import localizeOptions
from clientConsts import INPUT_SYSTEM_PROFILES, CONTROLS_GROUPS, INPUT_SYSTEM_PROFILES_REV
from debug_utils import LOG_ERROR, LOG_DEBUG
import InputMapping
import VOIP
from consts import INPUT_SYSTEM_STATE, INPUT_SYSTEM_PROFILES_LIST, HORIZONTAL_AXIS, VERTICAL_AXIS, ROLL_AXIS, FORCE_AXIS, FLAPS_AXIS, INPUT_SYSTEM_PROFILES_LIST_REVERT
from gui.Scaleform.GameOptions.vo.ControlSettingsVO import GroupControlVO
from gui.Scaleform.GameOptions.vo.ControlSettingsVO import CommandVO
from gui.Scaleform.GameOptions.vo.ControlSettingsVO import ButtonEntryVO
import Settings
from copy import copy
ALL_CONTROLS_GROUPS = copy(CONTROLS_GROUPS)
ALL_CONTROLS_GROUPS.append('SETTINGS_BASIC')

class JoystickPrimaryProfileLoader(BaseLoader):

    def load(self, profileVO, profilePrimary, settings):
        pass


class JoystickPrimaryPresetLoader(BaseLoader):

    def load(self, profileVO, profilePrimary):
        profileVO.inertiaCameraRoll = profilePrimary.INERTIA_CAMERA_ROLL
        profileVO.sensitivityInSniperMode = profilePrimary.SENSITIVITY_IN_SNIPER_MODE
        profileVO.hutSpeed = profilePrimary.HATKA_MOVE_SPEED
        profileVO.maxForce = profilePrimary.POINT_OF_NORMAL_THRUST
        profileVO.slipCompensationValue = profilePrimary.SLIP_COMPENSATION_VALUE
        profileVO.inertiaCamera = profilePrimary.INERTIA_CAMERA
        for flashKey, settingsKey in JOYSTICK_DATA_CURVE.iteritems():
            setattr(profileVO, flashKey, [ list(el) for el in getattr(profilePrimary, settingsKey).getPoints() ])


class GamepadPrimaryPresetLoader(BaseLoader):

    def load(self, profileVO, profilePrimary):
        profileVO.sensitivity = profilePrimary.SENSITIVITY
        profileVO.allCurves = list()
        profileVO.maxForce = profilePrimary.POINT_OF_NORMAL_THRUST
        profileVO.allowLead = profilePrimary.ALLOW_LEAD
        profileVO.cameraType = profilePrimary.CAMERA_TYPE
        profileVO.commonAxisInverted = profilePrimary.INVERT_G_VERTICAL
        profileVO.commonAxisDeadzone = profilePrimary.G_VERTICAL_DEAD_ZONE
        profileVO.safeRollOnLowAltitude = profilePrimary.SAFE_ROLL_ON_LOW_ALTITUDE
        profileVO.automaticFlaps = profilePrimary.AUTOMATIC_FLAPS
        profileVO.supermouseCameraFlexibility = profilePrimary.CAMERA_FLEXIBILITY
        profileVO.radiusOfConducting = profilePrimary.RADIUS_OF_CONDUCTING
        profileVO.supermouseEqualizerForce = profilePrimary.EQUALIZER_FORCE
        profileVO.supermouseEqualizerZoneSize = profilePrimary.EQUALIZER_ZONE_SIZE
        profileVO.supermouseRollSpeed = profilePrimary.ROLL_SPEED_CFC
        profileVO.supermouseRotationZoneDepth = profilePrimary.SHIFT_TURN
        profileVO.cameraAcceleration = profilePrimary.CAMERA_ACCELERATION
        profileVO.cameraRollSpeed = profilePrimary.CAMERA_ROLL_SPEED
        profileVO.cameraAngle = profilePrimary.CAMERA_ANGLE
        for flashKey, settingsKey in GAMEPAD_DIRECT_DATA_CURVE.iteritems():
            setattr(profileVO, flashKey, [ list(el) for el in getattr(profilePrimary, settingsKey).getPoints() ])


class MousePrimaryProfileLoader(BaseLoader):

    def load(self, profileVO, profilePrimary, settings):
        profileVO.mouseSensitivity = settings.mouseSensitivity


class MousePrimaryPresetLoader(BaseLoader):

    def load(self, profileVO, profilePrimary):
        profileVO.cameraType = profilePrimary.CAMERA_TYPE
        profileVO.mouseInvertVert = profilePrimary.MOUSE_INVERT_VERT
        profileVO.safeRollOnLowAltitude = profilePrimary.SAFE_ROLL_ON_LOW_ALTITUDE
        profileVO.allowLead = profilePrimary.ALLOW_LEAD
        profileVO.automaticFlaps = profilePrimary.AUTOMATIC_FLAPS
        if hasattr(profilePrimary, MOUSE_INTENSITY_SPLINE_KEY):
            points = getattr(profilePrimary, MOUSE_INTENSITY_SPLINE_KEY).p
            for i, key in enumerate(MOUSE_TIGHTENING_KEYS):
                getattr(profileVO, key).x, getattr(profileVO, key).y = points[i].x, points[i].y

        profileVO.supermouseCameraFlexibility = profilePrimary.CAMERA_FLEXIBILITY
        profileVO.radiusOfConducting = profilePrimary.RADIUS_OF_CONDUCTING
        profileVO.supermouseEqualizerForce = profilePrimary.EQUALIZER_FORCE
        profileVO.supermouseEqualizerZoneSize = profilePrimary.EQUALIZER_ZONE_SIZE
        profileVO.supermouseRollSpeed = profilePrimary.ROLL_SPEED_CFC
        profileVO.supermouseRotationZoneDepth = profilePrimary.SHIFT_TURN
        profileVO.cameraRollSpeed = profilePrimary.CAMERA_ROLL_SPEED
        profileVO.cameraAngle = profilePrimary.CAMERA_ANGLE
        profileVO.cameraAcceleration = profilePrimary.CAMERA_ACCELERATION
        profileVO.methodOfMixing.index = profilePrimary.METHOD_OF_MIXING
        profileVO.methodOfMixing.data = [localizeOptions('SETTINGS_MOUSE_MIXING_ALWAYS'), localizeOptions('SETTINGS_MOUSE_MIXING_HALF'), localizeOptions('SETTINGS_MOUSE_MIXING_BATTLECAM_ONLY')]


class KeyboardPrimaryProfileLoader(BaseLoader):

    def load(self, profileVO, profilePrimary, settings):
        profileVO.slipCompensation = profilePrimary.SLIP_COMPENSATION
        profileVO.keyboardInvertVert = profilePrimary.INVERT_VERT
        profileVO.inertiaCamera = profilePrimary.INERTIA_CAMERA


def prepareControlsGroup(mapping, groupID, controls):
    for cmdID, record in mapping.iteritems():
        cmd = record['cmdName']
        cmdLabel = InputMapping.getCommandLocalization(cmd)
        if cmdLabel is not None and not ((cmdID == InputMapping.CMD_PUSH_TO_TALK or cmdID == InputMapping.CMD_PUSH_TO_TALK_SQUAD or cmdID == InputMapping.CMD_TOGGLE_ARENA_VOICE_CHANNEL) and not VOIP.api().voipSupported):
            if groupID == InputMapping.g_descriptions.getCommandGroupID(cmd) or groupID == 'SETTINGS_BASIC' and record['isBase']:
                commandVO = CommandVO()
                commandVO.id = cmdID
                commandVO.title = cmdLabel
                commandVO.switchingStyle = record['switchingStyle']
                if isTutorial():
                    commandVO.enabled = cmd in Settings.g_instance.cmdFilter
                else:
                    commandVO.enabled = cmd not in Settings.g_instance.cmdFilter
                isFireAxis = len(record['linkedAxisName']) <= 0
                commandVO.axes.sign = record['fireAxisSign']
                if not isFireAxis:
                    commandVO.axes.axisDeadzone = record['linkedAxisDeadZone']
                    commandVO.axes.axisInverted = record['linkedAxisInverted']
                    commandVO.axes.axisSensitivity = record['linkedAxisSensitivity']
                    commandVO.axes.axisGroup = record['linkedAxisName']
                    commandVO.axes.axisSmoothing = record['linkedAxisSmoothWindow']
                commandVO.axes.axisDeviceId = str(record['fireAxisDevice' if isFireAxis else 'linkedAxisDevice'])
                commandVO.axes.axisDeviceName = record['fireAxisDeviceName' if isFireAxis else 'linkedAxisDeviceName']
                commandVO.axes.axisId = record['fireAxisIndex' if isFireAxis else 'linkedAxisIndex']
                commandVO.axes.axisLabel = InputMapping.getAxisLocalization(commandVO.axes.axisId)
                for key in record['keyNames']:
                    buttonEntryVO = ButtonEntryVO()
                    buttonEntryVO.id = key['name']
                    buttonEntryVO.deviceId = str(key['device'])
                    buttonEntryVO.label = InputMapping.getKeyLocalization(key['name'])
                    commandVO.buttons.append(buttonEntryVO)

                controls.append(commandVO)

    return


def prepareControls(mapping, container):
    for groupID in ALL_CONTROLS_GROUPS:
        o = GroupControlVO()
        o.id = groupID
        o.title = localizeOptions(groupID)
        prepareControlsGroup(mapping, groupID, o.controls)
        container.append(o)


class ControlProfileLoader(BaseLoader):

    def load(self, src):
        profiles = InputMapping.g_instance.getProfileNames()
        curProfileName = InputMapping.g_instance.getCurProfileName()
        profilesSorted = [ profileName for profileName in ORDER_PROFILES if profileName in profiles ]
        for profileName in profiles:
            if profileName not in profilesSorted:
                profilesSorted.append(profileName)
                LOG_DEBUG('__sendInputConfig - profileName(%s) was added to list without sorting' % profileName)

        curProfileIndex = 0
        for profile in profilesSorted:
            if profile in INPUT_SYSTEM_PROFILES_LIST:
                profileID = INPUT_SYSTEM_PROFILES_LIST[profile]
                if profileID not in INPUT_SYSTEM_PROFILES:
                    LOG_ERROR('__sendInputConfig - profileID(%s) not in INPUT_SYSTEM_PROFILES(%s)' % (profileID, INPUT_SYSTEM_PROFILES))
                keyValue = KeyValue()
                keyValue.key = INPUT_SYSTEM_PROFILES[profileID]
                keyValue.label = localizeOptions('CONTROL_PROFILE_%s' % profile.upper())
                src.controlProfiles.data.append(keyValue)
                if curProfileName == profile:
                    src.controlProfiles.index = curProfileIndex
                curProfileIndex += 1
            else:
                LOG_DEBUG('__sendInputConfig - %s not in INPUT_SYSTEM_PROFILES_LIST' % profile)


class ControlConstantsLoader(BaseLoader):

    def load(self, container):
        container.turnGamepadCmd = InputMapping.CMD_GAMEPAD_TURN_LEFT
        container.pitchGamepadCmd = InputMapping.CMD_GAMEPAD_PITCH_DOWN
        container.rollGamepadCmd = InputMapping.CMD_ROLL_LEFT
        container.forceGamepadCmd = InputMapping.CMD_INCREASE_FORCE
        container.cmdFreeVerticalCam = InputMapping.CMD_FREE_VERTICAL_CAM_GAMEPA
        container.cmdFreeHorizontalCam = InputMapping.CMD_FREE_HORIZONTAL_CAM_GAMEPAD
        container.rollCmd = InputMapping.CMD_ROLL_LEFT
        container.pitchCmd = InputMapping.CMD_PITCH_DOWN
        container.turnCmd = InputMapping.CMD_TURN_LEFT
        container.forceCmd = InputMapping.CMD_INCREASE_FORCE
        container.cmdFreeVerticalCamDesc = localizeOptions('TOOLTIP_SETTINGS_GAMEPAD_VERTICAL_VIEW')
        container.cmdFreeHorizontalCamDesc = localizeOptions('TOOLTIP_SETTINGS_GAMEPAD_HORIZONTAL_VIEW')
        container.rollCmdDesc = localizeOptions('TOOLTIP_SETTINGS_GAMEPAD_ROLL')
        container.pitchCmdDesc = localizeOptions('TOOLTIP_SETTINGS_JOYSTICK_VERTICAL_AXIS')
        container.turnCmdDesc = localizeOptions('TOOLTIP_SETTINGS_GAMEPAD_HORIZONTAL_AXIS')
        container.forceCmdDesc = localizeOptions('TOOLTIP_SETTINGS_GAMEPAD_THRUST')
        container.inputHorizontalAxisId = HORIZONTAL_AXIS
        container.inputVerticalAxisId = VERTICAL_AXIS
        container.inputRollAxisId = ROLL_AXIS
        container.inputForceAxisId = FORCE_AXIS
        container.inputFlapsAxisId = FLAPS_AXIS
        container.inputFreeVerticalCamGamepadAxisId = FLAPS_AXIS
        container.inputFreeHorizontalCamGamepadAxisId = FLAPS_AXIS
        container.freeVerticalCamGamepadCmd = InputMapping.CMD_FREE_VERTICAL_CAM_GAMEPA
        container.freeHorizontalCamGamepadCmd = InputMapping.CMD_FREE_HORIZONTAL_CAM_GAMEPAD


class ControlSettingsLoader(BaseLoader):

    def __init__(self, path):
        self._profilePrimaryLoaders = {INPUT_SYSTEM_STATE.JOYSTICK: JoystickPrimaryProfileLoader,
         INPUT_SYSTEM_STATE.MOUSE: MousePrimaryProfileLoader,
         INPUT_SYSTEM_STATE.KEYBOARD: KeyboardPrimaryProfileLoader}
        self._presetPrimaryLoaders = {INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL: GamepadPrimaryPresetLoader,
         INPUT_SYSTEM_STATE.JOYSTICK: JoystickPrimaryPresetLoader,
         INPUT_SYSTEM_STATE.MOUSE: MousePrimaryPresetLoader}
        self._profilePresetPrimaryLoaded = list()
        self._profilePrimaryLoaded = list()
        self._controlProfilesLoaded = False
        self._profilePresetArrayLoaded = list()
        self._profileKeyboardLoaded = list()
        BaseLoader.__init__(self, path)

    def destroy(self):
        self._profilePrimaryLoaders.clear()
        self._presetPrimaryLoaders.clear()

    def load(self, src, pList, settings, forceLoad):
        if not self._controlProfilesLoaded:
            self._controlProfilesLoaded = True
            ControlProfileLoader('controlProfiles').load(src)
            ControlConstantsLoader('controlConstants').load(src.controlConstants)
        src.fastFM = settings.gameUI['fastFM']
        if pList:
            fProfileName = pList[0]
            profileID = INPUT_SYSTEM_PROFILES_REV.get(fProfileName, None)
            if profileID is None:
                LOG_ERROR('load - bad fProfileName', fProfileName)
                return
            profileVO = getattr(src, INPUT_SYSTEM_PROFILES.get(profileID), None)
            if profileVO is None:
                LOG_ERROR('load - bad profileName', fProfileName, profileID)
                return
            profileName = INPUT_SYSTEM_PROFILES_LIST_REVERT.get(profileID)
            profileType = settings.getControlType()
            loaderProfilePrimaryClass = self._profilePrimaryLoaders.get(profileID, None)
            if loaderProfilePrimaryClass is not None:
                if profileName not in self._profilePrimaryLoaded:
                    profilePrimary = InputMapping.g_instance.getPrimaryFromProfile(profileName, profileType)
                    loaderProfilePrimaryClass('profilePrimary').load(profileVO, profilePrimary, settings)
                    self._profilePrimaryLoaded.append(profileName)
            if profileID == INPUT_SYSTEM_STATE.MOUSE:
                self._loadKeyboard(profileName, profileType, profileVO)
            loaderProfilePresetPrimaryClass = self._presetPrimaryLoaders.get(profileID, None)
            if loaderProfilePresetPrimaryClass is not None:
                self._loadPresetsArray(settings, profileName, profileID, profileVO)
                fPresetName = pList[1] if len(pList) > 1 else None
                if fPresetName is None:
                    LOG_DEBUG('load - without load preset data', profileName, fPresetName)
                    return
                presetName = ALL_PRESETS_KEYS[profileID][fPresetName] if fPresetName in ALL_PRESETS_KEYS[profileID] else None
                if presetName is not None and loaderProfilePresetPrimaryClass is not None:
                    if presetName not in self._profilePresetPrimaryLoaded:
                        profilePrimary = InputMapping.g_instance.getPrimaryFromProfile(presetName, profileType)
                        loaderProfilePresetPrimaryClass('profilePresetPrimary').load(getattr(profileVO, fPresetName), profilePrimary)
                        self._profilePresetPrimaryLoaded.append(presetName)
                if profileID != INPUT_SYSTEM_STATE.MOUSE:
                    self._loadKeyboard(presetName, profileType, getattr(profileVO, fPresetName))
            else:
                self._loadKeyboard(profileName, profileType, profileVO)
        return

    def _loadKeyboard(self, profileName, profileType, profileVO):
        if profileName not in self._profileKeyboardLoaded:
            profilePrimary = InputMapping.g_instance.getPrimaryFromProfile(profileName, profileType)
            profileKeyboard = InputMapping.g_instance.getKeyboardFromProfile(profileName, profileType)
            prepareControls(profileKeyboard.getCurMapping(profilePrimary), profileVO.groupControls)
            self._profileKeyboardLoaded.append(profileName)

    def _loadPresetsArray(self, settings, profileName, profileID, profileVO):
        if profileName not in self._profilePresetArrayLoaded:
            self._profilePresetArrayLoaded.append(profileName)
            presets = settings.inputProfilesPresets.get(profileName, None)
            if presets is not None:
                for i, preset in enumerate(presets):
                    presetName = preset['name']
                    presetID = len(profileVO.profilePreset.data)
                    if settings.inputProfilesPresetsCurrent[profileName] == presetName:
                        profileVO.profilePreset.index = i
                    flashKey = ALL_PRESETS_KEYS_REVERT[profileID].get(presetName)
                    if flashKey is not None:
                        keyValue = KeyValue()
                        keyValue.key = flashKey
                        keyValue.label = localizeOptions(preset['localizationID'])
                        profileVO.profilePreset.data.append(keyValue)
                        profilePresetVO = getattr(profileVO, flashKey)
                        profilePresetVO.id = presetID

        return