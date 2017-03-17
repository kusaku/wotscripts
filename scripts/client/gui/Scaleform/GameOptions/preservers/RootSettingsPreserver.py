# Embedded file name: scripts/client/gui/Scaleform/GameOptions/preservers/RootSettingsPreserver.py
__author__ = 's_karchavets'
from debug_utils import LOG_ERROR, LOG_WARNING
from gui.Scaleform.GameOptions.utils import BasePreserver, XMPP_CHAT_KEYS, GAMEPAD_DIRECT_DATA_CURVE, GAME_SETTINGS_MAIN_UI_DATA
from gui.Scaleform.GameOptions.utils import GRAPHICS_QUALITY_KEYS, VOIP_SETTINGS_DICT, ALL_PRESETS_KEYS_REVERT, ALL_PRESETS_KEYS
from gui.Scaleform.GameOptions.utils import MOUSE_TIGHTENING_KEYS, JOYSTICK_DATA_CURVE, JOY_DATA, MOUSE_DATA, KEYBOARD_DATA, GAMEPAD_DIRECT_CONTROL_DATA, DEVICES_UI_DATA, DEVICES_MAIN_UI_DATA, GENERAL_MAIN_UI_DATA, GENERAL_MAIN_SETTINGS_DATA, FP_SETTINGS, AIMS_KEYS
from gui.Scaleform.GameOptions.preservers.HudSettingsPreserver import *
from gui.Scaleform.GameOptions.preservers.GraphicSettingsPreserver import *
from gui.Scaleform.GameOptions.preservers.SoundSettingsPreserver import *
from gui.Scaleform.GameOptions.preservers.ControlSettingsPreserver import *
from gui.Scaleform.GameOptions.preservers.SignalsPreserver import *
from gui.Scaleform.GameOptions.preservers.GameSettingsPreserver import *
import InputMapping
import Settings
from clientConsts import AIMS_LOC, SOUND_SETTINGS_DICT, INPUT_SYSTEM_PROFILES
from consts import INPUT_SYSTEM_STATE, INPUT_SYSTEM_PROFILES_LIST_REVERT

class BaseListener(dict):

    def __init__(self):
        dict.__init__(self)
        self.activate = False
        self.__called = False

    @property
    def called(self):
        return self.__called

    def __getitem__(self, item):
        if self.activate:
            self.__called = True
        return dict.__getitem__(self, item)


class RootSettingsPreserver(BasePreserver):

    def __init__(self):
        self.__preservers = BaseListener()
        self.__preservers['signals'] = BaseListener()
        self.__preservers['settings'] = BaseListener()
        self.__preservers['settings']['soundSettings'] = BaseListener()
        self.__preservers['settings']['gameSettings'] = BaseListener()
        self.__preservers['settings']['graphicSettings'] = BaseListener()
        self.__preservers['settings']['controlSettings'] = BaseListener()
        self.__preservers['settings']['hudSettings'] = BaseListener()
        self.__prepareSignals(self.__preservers['signals'])
        self.__prepareHudSettings(self.__preservers['settings']['hudSettings'])
        self.__prepareGameSettings(self.__preservers['settings']['gameSettings'])
        self.__prepareSoundSettings(self.__preservers['settings']['soundSettings'])
        self.__prepareGraphicSettings(self.__preservers['settings']['graphicSettings'])
        self.__prepareControlSettings(self.__preservers['settings']['controlSettings'])
        self.__activate(self.__preservers, True)

    def __activate(self, preservers, isActive):
        for v in preservers.itervalues():
            if isinstance(v, BaseListener):
                v.activate = isActive
                self.__activate(v, isActive)

    def deactivate(self):
        self.__activate(self.__preservers, False)

    @property
    def listeners(self):
        return self.__preservers

    def destroy(self):
        self.__preservers = None
        return

    def __prepareControlSettings(self, controlS):
        for profileID, flashProfileName in INPUT_SYSTEM_PROFILES.iteritems():
            controlS[flashProfileName] = BaseListener()
            if profileID in [INPUT_SYSTEM_STATE.KEYBOARD, INPUT_SYSTEM_STATE.MOUSE]:
                controlS[flashProfileName]['groupControls'] = InputCommandPreserver(INPUT_SYSTEM_PROFILES_LIST_REVERT[profileID])
            if profileID == INPUT_SYSTEM_STATE.KEYBOARD:
                self.__addPrimaryPreserver(controlS[flashProfileName], KEYBOARD_DATA, profileID)
            else:
                controlS[flashProfileName]['profilePreset'] = BaseListener()
                controlS[flashProfileName]['profilePreset']['index'] = ProfilePresetPreserver(INPUT_SYSTEM_PROFILES_LIST_REVERT[profileID])
                for flashKey, presetID in ALL_PRESETS_KEYS[profileID].iteritems():
                    controlS[flashProfileName][flashKey] = BaseListener()
                    if profileID != INPUT_SYSTEM_STATE.MOUSE:
                        controlS[flashProfileName][flashKey]['groupControls'] = InputCommandPreserver(presetID)
                    if profileID == INPUT_SYSTEM_STATE.MOUSE:
                        self.__addPrimaryPreserver(controlS[flashProfileName][flashKey], MOUSE_DATA, profileID)
                        for i, primaryKey in enumerate(MOUSE_TIGHTENING_KEYS):
                            controlS[flashProfileName][flashKey][primaryKey] = MousePointsPreserver(presetID, primaryKey)

                        controlS[flashProfileName][flashKey]['methodOfMixing'] = BaseListener()
                        controlS[flashProfileName][flashKey]['methodOfMixing']['index'] = MethodOfMixingPreserver(INPUT_SYSTEM_PROFILES_LIST_REVERT[profileID])
                    elif profileID == INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL:
                        self.__addPrimaryPreserver(controlS[flashProfileName][flashKey], GAMEPAD_DIRECT_CONTROL_DATA, profileID)
                        for curveFlashKey, curveSettingsKey in GAMEPAD_DIRECT_DATA_CURVE.iteritems():
                            controlS[flashProfileName][flashKey][curveFlashKey] = JoystickPointsPreserver(presetID, curveSettingsKey)

                    elif profileID == INPUT_SYSTEM_STATE.JOYSTICK:
                        self.__addPrimaryPreserver(controlS[flashProfileName][flashKey], JOY_DATA, profileID)
                        for curveFlashKey, curveSettingsKey in JOYSTICK_DATA_CURVE.iteritems():
                            controlS[flashProfileName][flashKey][curveFlashKey] = JoystickPointsPreserver(presetID, curveSettingsKey)

            if profileID == INPUT_SYSTEM_STATE.MOUSE:
                controlS[flashProfileName]['mouseSensitivity'] = SettingsMainPreserver('mouseSensitivity')

        controlS['fastFM'] = ActiveFastFMPreserver()
        controlS['controlProfiles'] = ControlProfilesPreserver()

    def __prepareGraphicSettings(self, gs):
        gs['waitVSync'] = VideoVSyncPreserver()
        gs['graphicsGamma'] = GammaPreserver()
        gs['gsAutodetectEnabled'] = SettingsMainPreserver('gsAutodetectEnabled')
        gs['graphicsQuality'] = BaseListener()
        gs['graphicsQuality']['index'] = GraphicsQualityPreserver()
        gs['videoMode'] = VideoModePreserver()
        gs['graphicProfiles'] = BaseListener()
        gs['graphicProfiles']['graphicsCustomProfile'] = BaseListener()
        for quality_pythonKey, quality_flashKey in GRAPHICS_QUALITY_KEYS.iteritems():
            gs['graphicProfiles']['graphicsCustomProfile'][quality_flashKey] = BaseListener()
            gs['graphicProfiles']['graphicsCustomProfile'][quality_flashKey]['setting'] = BaseListener()
            gs['graphicProfiles']['graphicsCustomProfile'][quality_flashKey]['setting']['index'] = GraphicsDetailPreserver('custom', quality_pythonKey)

    def __prepareSoundSettings(self, ss):
        ss['qualitySound'] = BaseListener()
        ss['qualitySound']['index'] = QualitySoundPreserver()
        ss['soundType'] = BaseListener()
        ss['soundType']['index'] = TypeSoundPreserver()
        for flashKey, SettingsKey in SOUND_SETTINGS_DICT.iteritems():
            ss[flashKey] = SoundCategoryVolumePreserver(SettingsKey)

        for flashKey, SettingsKey in Settings.SOUND_PARAMETERS.iteritems():
            ss[flashKey] = SoundCategoryEnabledPreserver(SettingsKey)

        for flashKey, SettingsKey in Settings.VOIP_PARAMETERS_DICT.iteritems():
            if SettingsKey == 'captureDevice':
                ss[flashKey] = BaseListener()
                ss[flashKey]['index'] = VoiceChatMicDevicePreserver(SettingsKey)
            else:
                ss[flashKey] = VoipSoundPreserver(SettingsKey, VOIP_SETTINGS_DICT.get(flashKey, None))

        return

    def __prepareGameSettings(self, gameS):
        gameS['measurementSystem'] = BaseListener()
        gameS['measurementSystem']['index'] = GameUISettingsPreserver('measurementSystem')
        for flashKey, SettingsKey in XMPP_CHAT_KEYS.iteritems():
            gameS[flashKey] = GameSettingsPreserver(SettingsKey)

        for key in Settings.REPLAY_KEYS.iterkeys():
            gameS[key] = BattleReplaysPreserver(key)

        for fKey, sKey in GAME_SETTINGS_MAIN_UI_DATA.iteritems():
            gameS[fKey] = GameUISettingsPreserver(sKey)

        gameS['lobbySettings'] = BaseListener()
        gameS['lobbySettings']['hangar'] = HungarTypePreserver()

    def __prepareSignals(self, signalsS):
        signalsS['signalVoiceChatTest'] = SignalVoiceChatTestPreserver()
        signalsS['signalVoiceChatRefreshDevices'] = SignalVoiceChatRefreshDevicesPreserver()

    def __prepareHudSettings(self, hudS):
        for key in ['general',
         'devices',
         'aim',
         'markers',
         'forestallingPoint']:
            hudS[key] = BaseListener()

        for fKey, sKey in FP_SETTINGS.iteritems():
            hudS['forestallingPoint'][fKey] = SettingsMainPreserver(sKey)

        hudS['forestallingPoint']['colorPoint'] = BaseListener()
        hudS['forestallingPoint']['colorPoint']['index'] = SettingsMainPreserver('colorPointIndexFP')
        for key, profileName in AIMS_KEYS.iteritems():
            hudS['aim'][key] = BaseListener()
            for sub_key in AIMS_LOC.iterkeys():
                hudS['aim'][key][sub_key] = BaseListener()
                hudS['aim'][key][sub_key]['index'] = SettingsAimsPreserver(sub_key, profileName)

            for sub_key in ['crosshairTransparency',
             'targetAreaTransparency',
             'externalAimTransparency',
             'dynamycAim']:
                hudS['aim'][key][sub_key] = SettingsAimsPreserver(sub_key, profileName)

        for fKey, sKey in GENERAL_MAIN_UI_DATA.iteritems():
            hudS['general'][fKey] = GameUISettingsPreserver(sKey)

        for fKey, sKey in GENERAL_MAIN_SETTINGS_DATA.iteritems():
            hudS['general'][fKey] = SettingsMainPreserver(sKey)

        for fKey, sKey in DEVICES_MAIN_UI_DATA.iteritems():
            hudS['devices'][fKey] = GameUISettingsPreserver(sKey)

        for fKey, sKey in DEVICES_UI_DATA.iteritems():
            hudS['devices'][fKey] = BaseListener()
            hudS['devices'][fKey]['index'] = GameUISettingsPreserver(sKey)

        hudS['markers']['templates'] = MarkersPreserver()
        hudS['markers']['selectIDS'] = MarkerSelectPreserver()

    def __addPrimaryPreserver(self, srcContainer, attrContainer, profileID):
        for fKey, sKey in attrContainer.iteritems():
            srcContainer[fKey] = PrimaryPreserver(INPUT_SYSTEM_PROFILES_LIST_REVERT[profileID], sKey)