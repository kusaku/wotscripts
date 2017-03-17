# Embedded file name: scripts/client/gui/Scaleform/GameOptions/loaders/SoundSettingsLoader.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BaseLoader, SOUND_TYPE_LOC
from clientConsts import SOUND_SETTINGS_DICT, SOUND_QUALITY_IDX_DICT, QUALITY_SOUND_LOC
from Helpers.i18n import localizeOptions
import Settings
import InputMapping
import VOIP

class SoundSettingsLoader(BaseLoader):
    IS_VOICE_CHAT_DEVICES_REFRESHED = False

    def destroy(self):
        SoundSettingsLoader.IS_VOICE_CHAT_DEVICES_REFRESHED = False
        BaseLoader.destroy(self)

    def load(self, src, pList, settings, forceLoad):
        if not SoundSettingsLoader.IS_VOICE_CHAT_DEVICES_REFRESHED:
            SoundSettingsLoader.IS_VOICE_CHAT_DEVICES_REFRESHED = True
            VOIP.api().requestCaptureDevices()
        for flashKey, SettingsKey in SOUND_SETTINGS_DICT.iteritems():
            setattr(src, flashKey, settings.getSoundSettings()['volume'][SettingsKey])

        for flashKey, SettingsKey in Settings.SOUND_PARAMETERS.iteritems():
            setattr(src, flashKey, settings.getSoundSettings()['volumeEnabled'][SettingsKey])

        voipPrefs = settings.getVoipSettings()
        for flashKey, SettingsKey in Settings.VOIP_PARAMETERS_DICT.iteritems():
            if SettingsKey == 'isVoipEnabled':
                src.enableVoiceChat = voipPrefs[SettingsKey] and VOIP.api().voipSupported
            elif SettingsKey == 'captureDevice':
                src.voiceChatMicDevice.index = -1
                src.voiceChatMicDevice.data = [voipPrefs[SettingsKey]]
            else:
                setattr(src, flashKey, voipPrefs[SettingsKey])

        src.voiceChatMicActivationButtonId = InputMapping.CMD_PUSH_TO_TALK
        src.voiceChatMicActivationButtonId2 = InputMapping.CMD_PUSH_TO_TALK_SQUAD
        src.voiceChatMicActivationButtonId3 = InputMapping.CMD_TOGGLE_ARENA_VOICE_CHANNEL
        src.isVoiceChatVisible = VOIP.api().voipSupported
        src.isArenaVoiceChatVisible = VOIP.api().arenaChannelSupported
        src.qualitySound.data = [ localizeOptions(quality) for quality in QUALITY_SOUND_LOC ]
        src.qualitySound.index = SOUND_QUALITY_IDX_DICT[settings.getSoundSettings()['quality']]
        src.soundType.data = [ localizeOptions(id) for id in SOUND_TYPE_LOC ]
        src.soundType.index = settings.getSoundSettings()['speakerPreset']
        self._isLoaded = True