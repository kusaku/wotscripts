# Embedded file name: scripts/client/gui/Scaleform/GameOptions/loaders/SignalsLoader.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BaseLoader
import VOIP
import Settings
import BattleReplay

class SignalVoiceChatTestLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        VOIP.api().localTestMode = not VOIP.api().localTestMode


class SignalVoiceChatRefreshDevicesLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        VOIP.api().requestCaptureDevices()


class SignalGSAutodetectLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        Settings.g_instance.detectBestSettingsAdv()


class SignalReplaysIsActiveLoader(BaseLoader):

    def load(self, src, pList, settings, forceLoad):
        src.isActive = BattleReplay.isPlaying()