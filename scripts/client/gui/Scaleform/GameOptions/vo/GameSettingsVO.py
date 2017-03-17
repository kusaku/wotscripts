# Embedded file name: scripts/client/gui/Scaleform/GameOptions/vo/GameSettingsVO.py
__author__ = 's_karchavets'
from gui.Scaleform.GameOptions.utils import ArrayIndex

class LobbySettingsVO:

    def __init__(self):
        self.isEnabled = False
        self.hangar = ArrayIndex()
        self.previewImg = []


class GameSettingsVO:

    def __init__(self):
        self.isLazy = False
        self.measurementSystem = ArrayIndex()
        self.invitationsOnlyFromContactList = False
        self.messageCensureActive = False
        self.messageDateVisible = False
        self.messagesOnlyFromContactList = False
        self.ingnoreListVisible = False
        self.onlineListVisible = False
        self.saveBattleReplays = True
        self.removeBattleReplays = True
        self.daysForRemoveBattleReplays = 30
        self.pathSaveBattleReplays = ''
        self.isChatEnabled = True
        self.lobbySettings = LobbySettingsVO()