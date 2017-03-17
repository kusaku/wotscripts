# Embedded file name: scripts/client/gui/Scaleform/GameOptions/utils.py
__author__ = 's_karchavets'
from debug_utils import LOG_WARNING
from clientConsts import WINDOW_RENDER_MODE
import BigWorld

def isTutorial():
    if hasattr(BigWorld.player(), 'controllers'):
        return 'tutorialManager' in BigWorld.player().controllers
    return False


def getListsIndexes(s):
    listsIndexes = list()
    i = 0
    for ch in s:
        if ch == '[':
            for j in range(i + 1, len(s)):
                if s[j] == ']':
                    listsIndexes.append(int(s[i + 1:j]))
                    break

        i += 1

    return (s[:s.find('[')] if listsIndexes else None, listsIndexes)


def parseBracket(s):
    listAttrName, listIndex = (None, None)
    lbracket = s.find('[')
    rbracket = s.find(']')
    if lbracket != -1:
        listAttrName = s[:lbracket]
        listIndex = s[lbracket + 1:rbracket]
    return (listAttrName, listIndex)


class BaseLoader(object):

    def __init__(self, path):
        self._path = path
        self._isLoaded = False
        self._allLoaders = self._buildLoaders()
        self._init()

    def isLoaded(self):
        return self._isLoaded

    def _init(self):
        if self._allLoaders is not None:
            for path, cls in self._allLoaders.iteritems():
                setattr(self, path, cls(path))

        return

    def _buildLoaders(self):
        return None

    def _getSettings(self):
        return None

    def load(self, src, pList, settings = None, forceLoad = False):
        if pList:
            o = getattr(self, pList[0], None)
            if o is not None:
                if not o.isLoaded() or forceLoad:
                    o.load(getattr(src, pList[0]), pList[1:], settings if settings is not None else self._getSettings(), forceLoad)
            else:
                LOG_WARNING('load - bad path', pList)
        elif not self.isLoaded() or forceLoad:
            if self._allLoaders is not None:
                for path in self._allLoaders.iterkeys():
                    self.load(src, [path], settings if settings is not None else self._getSettings(), forceLoad)

            self._isLoaded = True
        return

    def destroy(self):
        if self._allLoaders is not None:
            for path in self._allLoaders.iterkeys():
                getattr(self, path).destroy()

            self._allLoaders.clear()
        return

    def _isLoadedAll(self):
        for path in self._allLoaders.iterkeys():
            if not getattr(self, path).isLoaded():
                return False

        return True


class KeyValue:

    def __init__(self):
        self.isLazy = False
        self.key = -1
        self.label = None
        return


class ArrayIndex:

    def __init__(self):
        self.isLazy = False
        self.index = -1
        self.data = list()


class BasePreserver:

    def save(self, value):
        pass

    def destroy(self):
        pass


class Point:

    def __init__(self):
        self.isLazy = False
        self.x = -1
        self.y = -1


SOUND_TYPE_LOC = ['SOUND_TYPE_DEFAULT', 'SOUND_TYPE_LAPTOP', 'SOUND_TYPE_HEADPHONES']
JOYSTICK_DATA_CURVE = {'horisontalCurve': 'AXIS_X_CURVE',
 'verticalCurve': 'AXIS_Y_CURVE',
 'rollCurve': 'AXIS_Z_CURVE'}
GAMEPAD_DIRECT_DATA_CURVE = {'allCurves': 'AXIS_Y_CURVE'}
MOUSE_INTENSITY_SPLINE_KEY = 'MOUSE_INTENSITY_SPLINE'
MOUSE_TIGHTENING_KEYS = ['tighteningLeft',
 'tighteningLeftTop',
 'tighteningCenter',
 'tighteningRightBottom',
 'tighteningRight']
GRAPHICS_PRESET_KEYS = {'low': 'graphicsLowProfile',
 'medium': 'graphicsMediumProfile',
 'very high': 'graphicsVeryHightProfile',
 'very low': 'graphicsVeryLowProfile',
 'custom': 'graphicsCustomProfile',
 'high': 'graphicsHightProfile'}
GRAPHICS_PRESET_KEYS_REV = dict([ (value, key) for key, value in GRAPHICS_PRESET_KEYS.iteritems() ])
VIDE_MODES_KEYS_LOC = {WINDOW_RENDER_MODE.WRM_FULLSCREEN: 'SETTINGS_FULLSCREEN',
 WINDOW_RENDER_MODE.WRM_WINDOWED: 'SETTINGS_WINDOWED',
 WINDOW_RENDER_MODE.WRM_BORDERLESS: 'SETTINGS_BORDERLESS'}
GRAPHICS_QUALITY_KEYS = dict(FXAA='fxaa', BACKBUFER_QUALITY='backbuferQuality', OBJECT_CLIP='objectClip', TREES='trees', MOTIONBLUR='motionBlur', PARTICLES_QUALITY='particlesQuality', OBJECT_LOD='objectLod', TEXTURE_QUALITY='textureQuality', SHADOWS_QUALITY='shadowsQuality', TEXTURE_FILTERING='textureFiltering', VOLUMETRICCLOUDS='volumeTricClouds', POSTFX='postFX', WATER_QUALITY='waterQuality')
GRAPHICS_QUALITY_KEYS_REV = dict([ (value, key) for key, value in GRAPHICS_QUALITY_KEYS.iteritems() ])
ORDER_PROFILES = ['mouse_directional',
 'mouse_direct_control',
 'keyboard',
 'joystick',
 'gamepad_direct_control']
VOIP_SETTINGS_DICT = dict(voiceChatVoiceVolume='voiceVolume', voiceChatMicrophoneSensitivity='voiceActivationLevel', voiceChatAmbientVolume='muffledMasterVolume')
from consts import INPUT_SYSTEM_STATE
JOYSTICK_PRESETS_KEYS = {'joystickCustomPreset': 'joystick',
 'joystickLogitech3dxProPreset': 'joystick_1_Logitech_3dx_pro',
 'joystickThrustmasterT1600Preset': 'joystick_2_Thrustmaster_T_1600',
 'joystickThrustmasterTFlightStickXPreset': 'joystick_3_Thrustmaster_T_Flight_Stick_X',
 'joystickSaitekCyborgV1FlightStickPreset': 'joystick_5_Saitek_Cyborg_V_1_Flight_Stick'}
JOYSTICK_PRESETS_KEYS_REVERT = dict([ (value, key) for key, value in JOYSTICK_PRESETS_KEYS.iteritems() ])
GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS = {'gamepadCustomPreset': 'gamepad_direct_control',
 'gamepadDc1Xbox360Preset': 'gamepad_dc_1_xbox_360',
 'gamepadDc2Playstation23Preset': 'gamepad_dc_2_playstation_2_3',
 'gamepadDc3ThrustmasterDualTriggerRumbleForcePreset': 'gamepad_dc_4_Logitech_F310_510_710'}
GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS_REVERT = dict([ (value, key) for key, value in GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS.iteritems() ])
MOUSE_PRESETS_KEYS = {'mouseCustomPreset': 'mouse_directional',
 'mouseVectorPreset': 'mouse_directional_mouse1',
 'mouseHybridPreset': 'mouse_directional_mouse2',
 'mouseFreePreset': 'mouse_directional_mouse3',
 'mouseDefaultPreset': 'mouse_directional_mouse4',
 'mouseMouse5': 'mouse_directional_mouse5'}
MOUSE_PRESETS_KEYS_REVERT = dict([ (value, key) for key, value in MOUSE_PRESETS_KEYS.iteritems() ])
ALL_PRESETS_KEYS = {INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL: GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS,
 INPUT_SYSTEM_STATE.JOYSTICK: JOYSTICK_PRESETS_KEYS,
 INPUT_SYSTEM_STATE.MOUSE: MOUSE_PRESETS_KEYS}
ALL_PRESETS_KEYS_REVERT = {INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL: GAMEPAD_DIRECT_CONTROL_PRESETS_KEYS_REVERT,
 INPUT_SYSTEM_STATE.JOYSTICK: JOYSTICK_PRESETS_KEYS_REVERT,
 INPUT_SYSTEM_STATE.MOUSE: MOUSE_PRESETS_KEYS_REVERT}
JOY_DATA = {'inertiaCamera': 'INERTIA_CAMERA',
 'maxForce': 'POINT_OF_NORMAL_THRUST',
 'slipCompensationValue': 'SLIP_COMPENSATION_VALUE',
 'hutSpeed': 'HATKA_MOVE_SPEED',
 'inertiaCameraRoll': 'INERTIA_CAMERA_ROLL',
 'sensitivityInSniperMode': 'SENSITIVITY_IN_SNIPER_MODE'}
MOUSE_DATA = {'cameraType': 'CAMERA_TYPE',
 'supermouseCameraFlexibility': 'CAMERA_FLEXIBILITY',
 'radiusOfConducting': 'RADIUS_OF_CONDUCTING',
 'supermouseEqualizerForce': 'EQUALIZER_FORCE',
 'supermouseEqualizerZoneSize': 'EQUALIZER_ZONE_SIZE',
 'safeRollOnLowAltitude': 'SAFE_ROLL_ON_LOW_ALTITUDE',
 'supermouseRollSpeed': 'ROLL_SPEED_CFC',
 'supermouseRotationZoneDepth': 'SHIFT_TURN',
 'mouseInvertVert': 'MOUSE_INVERT_VERT',
 'automaticFlaps': 'AUTOMATIC_FLAPS',
 'cameraAcceleration': 'CAMERA_ACCELERATION',
 'cameraRollSpeed': 'CAMERA_ROLL_SPEED',
 'cameraAngle': 'CAMERA_ANGLE',
 'allowLead': 'ALLOW_LEAD',
 'methodOfMixing': 'METHOD_OF_MIXING'}
KEYBOARD_DATA = {'slipCompensation': 'SLIP_COMPENSATION',
 'keyboardInvertVert': 'INVERT_VERT',
 'inertiaCamera': 'INERTIA_CAMERA'}
GAMEPAD_DIRECT_CONTROL_DATA = {'maxForce': 'POINT_OF_NORMAL_THRUST',
 'allowLead': 'ALLOW_LEAD',
 'cameraType': 'CAMERA_TYPE',
 'commonAxisInverted': 'INVERT_G_VERTICAL',
 'commonAxisDeadzone': 'G_VERTICAL_DEAD_ZONE',
 'safeRollOnLowAltitude': 'SAFE_ROLL_ON_LOW_ALTITUDE',
 'automaticFlaps': 'AUTOMATIC_FLAPS',
 'supermouseCameraFlexibility': 'CAMERA_FLEXIBILITY',
 'radiusOfConducting': 'RADIUS_OF_CONDUCTING',
 'supermouseEqualizerForce': 'EQUALIZER_FORCE',
 'supermouseEqualizerZoneSize': 'EQUALIZER_ZONE_SIZE',
 'supermouseRollSpeed': 'ROLL_SPEED_CFC',
 'supermouseRotationZoneDepth': 'SHIFT_TURN',
 'cameraAcceleration': 'CAMERA_ACCELERATION',
 'cameraRollSpeed': 'CAMERA_ROLL_SPEED',
 'cameraAngle': 'CAMERA_ANGLE',
 'sensitivity': 'SENSITIVITY'}
DEVICES_UI_DATA = {'aviaHorizonType': 'horizonList',
 'playerListType': 'curPlayerListState',
 'heightMode': 'heightMode'}
DEVICES_MAIN_UI_DATA = {'playerList': 'players',
 'navigationWindowRadar': 'navigationWindowRadar',
 'navigationWindowMinimap': 'navigationWindowMinimap',
 'speedometerAndVariometer': 'speedometerAndVariometer',
 'combatInterfaceType': 'combatInterfaceType',
 'additionalView': 'targetWindow',
 'aviaHorizon': 'horizon'}
GENERAL_MAIN_UI_DATA = {'collisionWarningSystem': 'collisionWarningSystem',
 'alternativeColorMode': 'alternativeColorMode',
 'isSniperMode': 'isSniperMode'}
GENERAL_MAIN_SETTINGS_DATA = {'blockWinButton': 'blockWinButton',
 'blockAltTAB': 'blockAltTAB',
 'cinemaCamera': 'cinemaCamera',
 'cameraZoomType': 'cameraZoomType',
 'cameraEffectsEnabled': 'cameraEffectsEnabled',
 'preIntroEnabled': 'preIntroEnabled',
 'FOVCamera': 'maxMouseCombatFov'}
XMPP_CHAT_KEYS = {'messageCensureActive': 'messageFilterEnabled',
 'messagesOnlyFromContactList': 'notListenToAnonymous',
 'ingnoreListVisible': 'displayIgnoredContatcs',
 'onlineListVisible': 'disableOfflineContacts',
 'messageDateVisible': 'displayMessageTime'}
GAME_SETTINGS_MAIN_UI_DATA = {'isChatEnabled': 'isChatEnabled'}
FP_SETTINGS = {'isShowAdvancePoint': 'showAdvancePoint',
 'isToBoundary': 'isToBoundaryFP',
 'isSize': 'isSizeFP',
 'isBestTime': 'isBestTimeFP'}
AIMS_KEYS = {'mouseAim': 'mouse_directional',
 'joystickAim': 'joystick',
 'gamepadAim': 'gamepad_direct_control'}