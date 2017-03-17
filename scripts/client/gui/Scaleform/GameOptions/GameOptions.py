# Embedded file name: scripts/client/gui/Scaleform/GameOptions/GameOptions.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import isTutorial, ALL_PRESETS_KEYS, AIMS_KEYS
import BigWorld
from gui.Scaleform.windows import UIInterface
from debug_utils import LOG_DEBUG, LOG_ERROR
from gui.Scaleform.GameOptions.GameOptionsManager import GameOptionsManager
from gui.Scaleform.GameOptions.vo.Signals import SignalKeyVO, SignalAxisVO, SignalPreviewAxisVO
import GlobalEvents
import VOIP
import Settings
from copy import copy
import InputMapping
import GameEnvironment
import messenger
from consts import INPUT_SYSTEM_PROFILES_LIST_REVERT, INPUT_SYSTEM_STATE
from clientConsts import INPUT_SYSTEM_PROFILES
AXIS_SETUP_THRESHOLD = 0.45
DISABLED_KEYS = ['KEY_ESCAPE',
 'KEY_LWIN',
 'KEY_RWIN',
 'KEY_APPS',
 'KEY_DEBUG',
 'KEY_NUMLOCK',
 'KEY_SCROLL',
 'KEY_CAPSLOCK',
 'KEY_SYSRQ',
 'KEY_NONE',
 'KEY_RETURN',
 'KEY_NUMPADENTER']
NEED_SAVE_SOURCE_SETTINGS = False

class SETTINGS_TABS:
    CONTROLS = 'CONTROLS'
    GRAPHICS = 'GRAPHICS'
    AUDIO = 'AUDIO'
    HUD = 'HUD'
    GAME = 'GAME'


class GameOptions(UIInterface):

    def __init__(self):
        UIInterface.__init__(self)
        self.__externalCallbacks = {'settings.load': self.__load,
         'settings.save': self.__save,
         'settings.delete': self.__delete,
         'settings.switchTab': self.__switchTab}
        if not isTutorial():
            Settings.g_instance.cmdFilter += ['CMD_GAMEPAD_TURN_RIGHT',
             'CMD_GAMEPAD_TURN_LEFT',
             'CMD_GAMEPAD_PITCH_DOWN',
             'CMD_GAMEPAD_PITCH_UP',
             'CMD_FREE_VERTICAL_CAM_GAMEPA',
             'CMD_FREE_HORIZONTAL_CAM_GAMEPAD']
        self.__gameOptionsManager = GameOptionsManager(NEED_SAVE_SOURCE_SETTINGS)
        self.__voiceChatMicDeviceCallback = None
        return

    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.addExternalCallbacks(self.__externalCallbacks)
        GlobalEvents.onRefreshResolutions += self.__handleRefreshResolutions
        VOIP.api().eventCaptureDevicesUpdated += self.__onCaptureDevicesUpdated
        Settings.g_instance.eChangedGraphicsDetails += self.__onChangeGraphicsDetails
        InputMapping.g_instance.onProfileLoaded += self.__inputProfileChanged
        player = BigWorld.player()
        from Account import PlayerAccount
        if player is not None and player.__class__ == PlayerAccount:
            player.onInitPremium += self.__onPremiumChanged
        self.call_1('settings.initialized')

        class VirtualJoystickProfile:

            def __init__(self, sendPrimaryAxisCallBack):
                """
                @param sendPrimaryAxisCallBack: function (axis, value)
                """
                self.__sendPrimaryAxisCallBack = sendPrimaryAxisCallBack

            def sendPrimaryAxis(self, axis, value, rawValue):
                self.__sendPrimaryAxisCallBack(axis, value, rawValue)

            def dispose(self):
                self.__sendPrimaryAxisCallBack = None
                return

        self.__virtualJoystickProfile = VirtualJoystickProfile(self.__sendPrimaryAxis)
        from input.InputSubsystem.JoyInput import JoystickExpertInput
        self.__virtualJoystick = JoystickExpertInput(self.__virtualJoystickProfile)
        from input.InputSubsystem.GamepadInput import GamePadExpertInput
        self.__virtualGamePad = GamePadExpertInput(self.__virtualJoystickProfile)
        self.__virtualJoystick.setRawForceAxis(False)
        LOG_DEBUG('populateUI')
        return

    def dispossessUI(self):
        LOG_DEBUG('dispossessUI')
        self.__clearVoiceChatMicDeviceCallback()
        VOIP.api().localTestMode = False
        VOIP.api().clearEventCaptureDevicesUpdated()
        player = BigWorld.player()
        from Account import PlayerAccount
        if player is not None and player.__class__ == PlayerAccount:
            player.onInitPremium -= self.__onPremiumChanged
        Settings.g_instance.eChangedGraphicsDetails -= self.__onChangeGraphicsDetails
        GlobalEvents.onRefreshResolutions -= self.__handleRefreshResolutions
        InputMapping.g_instance.onProfileLoaded -= self.__inputProfileChanged
        for command in self.__externalCallbacks.iterkeys():
            self.uiHolder.removeExternalCallback(command)

        self.__externalCallbacks = None
        self.__eUpdateSettings()
        self.__gameOptionsManager.destroy()
        self.__gameOptionsManager = None
        Settings.g_instance.cmdFilter = list()
        self.__virtualJoystick.dispose()
        self.__virtualJoystick = None
        self.__virtualGamePad.dispose()
        self.__virtualGamePad = None
        self.__virtualJoystickProfile.dispose()
        self.__virtualJoystickProfile = None
        Settings.g_instance.save()
        UIInterface.dispossessUI(self)
        return

    def __inputProfileChanged(self):
        pass

    def __getProfilesForSave(self, settings):
        """
        get profiles/presets names for save to xml-files
        @param settings: <BaseListener>
        @return: <list>
        """

        def checkForSaveProfile(container, profileName):
            if profileName in InputMapping.g_instance.getProfileNames():
                container.append(profileName)

        profileNamesForSave = list()
        for profileID, flashProfileName in INPUT_SYSTEM_PROFILES.iteritems():
            profileData = settings.get(flashProfileName, None)
            if profileData is not None and profileData.called:
                presets = ALL_PRESETS_KEYS.get(profileID, None)
                if presets is not None:
                    for presetName in presets.itervalues():
                        checkForSaveProfile(profileNamesForSave, presetName)

                elif profileID in INPUT_SYSTEM_PROFILES_LIST_REVERT:
                    checkForSaveProfile(profileNamesForSave, INPUT_SYSTEM_PROFILES_LIST_REVERT[profileID])

        return profileNamesForSave

    def __eUpdateSettings(self):
        GameEnvironment.g_instance.eUpdateHUDSettings()
        self.__gameOptionsManager.preservers.deactivate()
        settings = self.__gameOptionsManager.preservers.listeners['settings']
        if settings['controlSettings'].called:
            profileNamesForSave = self.__getProfilesForSave(settings['controlSettings'])
            if profileNamesForSave:
                InputMapping.g_instance.saveControlls(profileNamesForSave)
            else:
                InputMapping.g_instance.onSaveControls()
        if settings['hudSettings']['markers'].called or settings['gameSettings']['measurementSystem'].called:
            GameEnvironment.g_instance.eMarkersSettingsUpdate()
        if settings['hudSettings']['aim'].called or settings['controlSettings'].called:
            Settings.g_instance.updatePointerVisibility()
            GameEnvironment.g_instance.eAimsSettingsUpdate()
        if settings['hudSettings']['general'].called or settings['hudSettings']['devices'].called or settings['gameSettings']['measurementSystem'].called:
            GameEnvironment.g_instance.eUpdateUIComponents()
        if settings['gameSettings'].called:
            messenger.g_xmppChatHandler.onUpdateChatSettings()

    def __onCaptureDevicesUpdated(self, devices, currentDevice):
        """
        event from VOIP
        @param devices: <list>
        @param currentDevice: <str> - value in devices
        """
        self.__clearVoiceChatMicDeviceCallback()
        voipPrefs = Settings.g_instance.getVoipSettings()
        if voipPrefs['captureDevice'] in devices:
            currentDevice = voipPrefs['captureDevice']
        Settings.g_instance.voipCaptureDevices = copy(devices)
        Settings.g_instance.setVoipValue('captureDevice', currentDevice)
        self.__gameOptionsManager.root.settings.soundSettings.voiceChatMicDevice.data = copy(devices)
        self.__gameOptionsManager.root.settings.soundSettings.voiceChatMicDevice.index = devices.index(currentDevice) if currentDevice in devices else -1
        path = 'settings.soundSettings.voiceChatMicDevice'
        self.__voiceChatMicDeviceCallback = BigWorld.callback(0.1, lambda : self.call_1('receive', path, self.__gameOptionsManager.load(path)))

    def __onPremiumChanged(self, isPremium, spaceData):
        p = 'settings.gameSettings.lobbySettings'
        self.__gameOptionsManager.loadSrc(p)
        data = self.__gameOptionsManager.load(p, False)
        self.call_1('receive', p, data)

    def __onChangeGraphicsDetails(self):
        p = 'settings.graphicSettings'
        self.__gameOptionsManager.loadSrc(p)
        self.call_1('receive', p, self.__gameOptionsManager.load(p, False))

    def __handleRefreshResolutions(self):
        resolutions, curResolutionIndex = Settings.g_instance.getVideoResolutions()
        self.__gameOptionsManager.root.settings.graphicSettings.videoMode.resolutions.index = curResolutionIndex
        self.__gameOptionsManager.root.settings.graphicSettings.videoMode.resolutions.data = copy(resolutions)
        self.__gameOptionsManager.root.settings.graphicSettings.videoMode.modes.index = Settings.g_instance.getWindowMode()
        path = 'settings.graphicSettings.videoMode'
        self.call_1('receive', path, self.__gameOptionsManager.load(path))

    def handleKeyEvent(self, event):
        keyName = InputMapping.getKeyNameByCode(event.key)
        if keyName is not None and keyName not in DISABLED_KEYS:
            if self.__gameOptionsManager.root.signals.signalKey.isSignalActive:
                signalKeyVO = SignalKeyVO()
                signalKeyVO.id = keyName
                signalKeyVO.isKeyDown = event.isKeyDown()
                signalKeyVO.isSignalActive = True
                signalKeyVO.deviceId = str(event.deviceId)
                signalKeyVO.deviceName = BigWorld.getDeviceName(event.deviceId)
                signalKeyVO.label = InputMapping.getKeyLocalization(keyName)
                self.call_1('receive', 'signals.signalKey', signalKeyVO)
                return True
        return False

    def handleAxisEvent(self, event):
        if self.__gameOptionsManager.root.signals.signalAxis.isSignalActive and abs(event.value) > AXIS_SETUP_THRESHOLD:
            signalAxis = SignalAxisVO()
            signalAxis.isSignalActive = True
            signalAxis.id = event.axis
            signalAxis.value = event.value
            signalAxis.deviceName = BigWorld.getDeviceName(event.deviceId)
            signalAxis.deviceId = str(event.deviceId)
            signalAxis.label = InputMapping.getAxisLocalization(event.axis)
            self.call_1('receive', 'signals.signalAxis', signalAxis)
        if self.__gameOptionsManager.root.signals.signalAxisPreview.isSignalActive:
            self.__currentAxisEvent(event)
        return True

    def __currentAxisEvent(self, event):
        profileName = InputMapping.g_instance.getCurProfileName()
        if profileName == INPUT_SYSTEM_PROFILES_LIST_REVERT[INPUT_SYSTEM_STATE.JOYSTICK]:
            self.__virtualJoystick.processJoystickEvent(event)
        elif profileName == INPUT_SYSTEM_PROFILES_LIST_REVERT[INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL]:
            self.__virtualGamePad.processJoystickEvent(event)

    def __sendPrimaryAxis(self, axis, value, rawValue):
        signalAxis = SignalPreviewAxisVO()
        signalAxis.isSignalActive = True
        signalAxis.inputAxisId = axis
        signalAxis.value = value
        signalAxis.rawValue = rawValue
        self.call_1('receive', 'signals.signalAxisPreview', signalAxis)

    def __load(self, path):
        LOG_DEBUG('__load', path)
        return self.__gameOptionsManager.load(path)

    def __save(self, path, obj):
        LOG_DEBUG('__save', path, obj)
        self.__gameOptionsManager.save(path, obj)

    def __delete(self, path, obj):
        LOG_DEBUG('__delete', path)
        self.__gameOptionsManager.delete(path, obj)

    def __clearVoiceChatMicDeviceCallback(self):
        if self.__voiceChatMicDeviceCallback is not None:
            BigWorld.cancelCallback(self.__voiceChatMicDeviceCallback)
            self.__voiceChatMicDeviceCallback = None
        return

    def __switchTab(self, tab):
        if tab != SETTINGS_TABS.AUDIO:
            self.__clearVoiceChatMicDeviceCallback()
            VOIP.api().localTestMode = False