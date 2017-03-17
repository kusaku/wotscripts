# Embedded file name: scripts/client/gui/Scaleform/GameOptions/preservers/GameSettingsPreserver.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import BasePreserver
import Settings
from consts import ZOOM_TYPES_KEYS, EMPTY_IDTYPELIST
from adapters.ICurrentHangarSpaceAdapter import ICurrentHangarSpacePreviewAdapter, ICurrentHangarSpaceAccountAdapter

class GameSettingsPreserver(BasePreserver):

    def __init__(self, key):
        self._key = key

    def save(self, value):
        Settings.g_instance.setXmppChatValue(self._key, value)


class GameUISettingsPreserver(BasePreserver):

    def __init__(self, key):
        self.__key = key

    def save(self, value):
        if self.__key == 'curPlayerListState':
            value += 1
        Settings.g_instance.setGameUIValue(self.__key, value)


class SettingsMainPreserver(BasePreserver):

    def __init__(self, key):
        self.__key = key

    def save(self, value):
        if self.__key == 'cameraZoomType':
            value = ZOOM_TYPES_KEYS[int(value)]
        Settings.g_instance.setMain(self.__key, value)


class BattleReplaysPreserver(BasePreserver):

    def __init__(self, key):
        self._key = key

    def save(self, value):
        Settings.g_instance.setReplayValue(self._key, value)


class HungarTypePreserver(BasePreserver):

    def save(self, value):
        i = value.index
        spaceID = value.data[i].key
        from gui.WindowsManager import g_windowsManager
        g_windowsManager.getAccountUI().deleteIFace([[{'ICurrentHangarSpace': {}}, [[None, 'preview']]]])
        g_windowsManager.getAccountUI().addIFace([[{'ICurrentHangarSpace': {'spaceID': spaceID}}, [[None, 'preview']]]])
        g_windowsManager.getAccountUI().editIFace([[{'ICurrentHangarSpace': {'spaceID': spaceID}}, EMPTY_IDTYPELIST]])
        return