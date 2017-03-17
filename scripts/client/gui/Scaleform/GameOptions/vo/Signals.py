# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/Signals.py
__author__ = 's_karchavets'

class SignalKeyVO:

    def __init__(self):
        self.isSignalActive = False
        self.id = -1
        self.deviceName = ''
        self.deviceId = ''
        self.label = ''
        self.isKeyDown = False


class SignalPreviewAxisVO:

    def __init__(self):
        self.isSignalActive = False
        self.inputAxisId = -1
        self.value = 0
        self.rawValue = 0


class SignalAxisVO:

    def __init__(self):
        self.isSignalActive = False
        self.id = -1
        self.value = 0
        self.deviceName = ''
        self.deviceId = ''
        self.label = ''


class SignalVoiceChatTestVO:

    def __init__(self):
        self.isSuccess = False


class SignalVoiceChatRefreshDevicesVO:

    def __init__(self):
        self.isSuccess = False


class SignalGSAutodetectVO:

    def __init__(self):
        self.isSuccess = False


class SignalReplaysIsActiveVO:

    def __init__(self):
        self.isActive = False


class SignalsVO:

    def __init__(self):
        self.signalKey = SignalKeyVO()
        self.signalAxis = SignalAxisVO()
        self.signalAxisPreview = SignalPreviewAxisVO()
        self.signalVoiceChatTest = SignalVoiceChatTestVO()
        self.signalVoiceChatRefreshDevices = SignalVoiceChatRefreshDevicesVO()
        self.signalGSAutodetectVO = SignalGSAutodetectVO()
        self.signalReplaysIsActive = SignalReplaysIsActiveVO()