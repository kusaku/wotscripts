# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/SoundSettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import ArrayIndex

class SoundSettingsVO:

    def __init__(self):
        self.isLazy = True
        self.masterVolume = 0.0
        self.musicVolume = 0.0
        self.voiceVolume = 0.0
        self.vehicleVolume = 0.0
        self.effectsVolume = 0.0
        self.interfaceVolume = 0.0
        self.ambientVolume = 0.0
        self.engineVolume = 0.0
        self.gunsVolume = 0.0
        self.isMasterVolume = True
        self.isMusicVolume = True
        self.isVoiceVolume = True
        self.isVehicleVolume = True
        self.isEffectsVolume = True
        self.isInterfaceVolume = True
        self.isAmbientVolume = True
        self.isEngineVolume = True
        self.isGunsVolume = True
        self.enableArenaVoiceChat = True
        self.voiceChatVoiceVolume = 0.0
        self.voiceChatMicrophoneSensitivity = 0.0
        self.voiceChatAmbientVolume = 0.0
        self.enableVoiceChat = False
        self.voiceChatMicDevice = ArrayIndex()
        self.voiceChatMicActivationButtonId = -1
        self.voiceChatMicActivationButtonId2 = -1
        self.voiceChatMicActivationButtonId3 = -1
        self.isVoiceChatVisible = False
        self.isArenaVoiceChatVisible = False
        self.qualitySound = ArrayIndex()
        self.soundType = ArrayIndex()