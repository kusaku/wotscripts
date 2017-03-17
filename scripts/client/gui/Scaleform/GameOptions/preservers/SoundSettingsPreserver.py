# Embedded file name: scripts/client/gui/Scaleform/GameOptions/preservers/SoundSettingsPreserver.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BasePreserver
from clientConsts import SOUND_QUALITY_IDX_DICT
import Settings
import VOIP

class TypeSoundPreserver(BasePreserver):

    def save(self, value):
        Settings.g_instance.setSoundSpeakerPreset(value)


class QualitySoundPreserver(BasePreserver):

    def save(self, value):
        Settings.g_instance.setQualitySound([ k for k, v in SOUND_QUALITY_IDX_DICT.iteritems() if v == int(value) ][0])


class SoundCategoryEnabledPreserver(BasePreserver):

    def __init__(self, key):
        self.__key = key

    def save(self, value):
        Settings.g_instance.setCategoryEnabled(self.__key, value)


class SoundCategoryVolumePreserver(BasePreserver):

    def __init__(self, key):
        self.__key = key

    def save(self, value):
        Settings.g_instance.setCategoryVolume(self.__key, value)


class VoipSoundPreserver(BasePreserver):

    def __init__(self, SettingsKey, voipKey):
        self.__SettingsKey = SettingsKey
        self.__voipKey = voipKey

    def save(self, value):
        Settings.g_instance.setVoipValue(self.__SettingsKey, value)
        if self.__SettingsKey == 'isVoipEnabled':
            VOIP.api().enabled = value
        else:
            key = self.__voipKey if self.__voipKey is not None else self.__SettingsKey
            kwargs = {key: value}
            VOIP.api().updateSettings(**kwargs)
        return


class VoiceChatMicDevicePreserver(BasePreserver):

    def __init__(self, key):
        self.__key = key

    def save(self, value):
        voipCaptureDevices = Settings.g_instance.voipCaptureDevices
        deviceIndex = int(value)
        if 0 <= deviceIndex < len(voipCaptureDevices):
            device = voipCaptureDevices[deviceIndex]
            Settings.g_instance.setVoipValue('captureDevice', device)
            VOIP.api().updateSettings(captureDevice=device)