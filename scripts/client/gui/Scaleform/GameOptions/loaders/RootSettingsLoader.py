# Embedded file name: scripts/client/gui/Scaleform/GameOptions/loaders/RootSettingsLoader.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.loaders.GameSettingsLoader import GameSettingsLoader
from gui.Scaleform.GameOptions.loaders.HUDSettingsLoader import HUDSettingsLoader
from gui.Scaleform.GameOptions.loaders.GraphicSettingsLoader import GraphicSettingsLoader
from gui.Scaleform.GameOptions.loaders.SoundSettingsLoader import SoundSettingsLoader
from gui.Scaleform.GameOptions.loaders.ControlSettingsLoader import ControlSettingsLoader
from gui.Scaleform.GameOptions.loaders.SignalsLoader import SignalVoiceChatTestLoader, SignalVoiceChatRefreshDevicesLoader, SignalGSAutodetectLoader, SignalReplaysIsActiveLoader
from gui.Scaleform.GameOptions.utils import BaseLoader
import Settings

class SettingsLoader(BaseLoader):

    def _buildLoaders(self):
        return dict(gameSettings=GameSettingsLoader, hudSettings=HUDSettingsLoader, graphicSettings=GraphicSettingsLoader, soundSettings=SoundSettingsLoader, controlSettings=ControlSettingsLoader)

    def isLoaded(self):
        return self._isLoadedAll()

    def _getSettings(self):
        if self._path == 'settingsDefault':
            return Settings.g_instance.defaultMain
        return Settings.g_instance


class SignalsLoader(BaseLoader):

    def _buildLoaders(self):
        return dict(signalVoiceChatTest=SignalVoiceChatTestLoader, signalVoiceChatRefreshDevices=SignalVoiceChatRefreshDevicesLoader, signalGSAutodetectVO=SignalGSAutodetectLoader, signalReplaysIsActive=SignalReplaysIsActiveLoader)


class RootSettingsLoader(BaseLoader):

    def _buildLoaders(self):
        return dict(settings=SettingsLoader, settingsDefault=SettingsLoader, settingsSource=SettingsLoader, signals=SignalsLoader)

    def isLoaded(self):
        return self._isLoadedAll()