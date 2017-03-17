# Embedded file name: scripts/client/gui/Scaleform/Interview.py
import BigWorld
from debug_utils import LOG_DEBUG, LOG_NOTE, LOG_INFO
from gui.Scaleform.windows import GUIWindowAccount
import db.DBLogic
import time
import re
import GlobalEvents
from Helpers.i18n import localizeMessages

class _PreviewVO:

    def __init__(self):
        self.title = ''
        self.question = ''
        self.arenaIcoPath = ''


class Interview(GUIWindowAccount):

    def __init__(self):
        GUIWindowAccount.__init__(self, 'interview.swf')

    def initialized(self):
        LOG_INFO('init Interview')
        self.addExternalCallbacks({'preview.answer': self.onAnswer})
        import BWPersonality
        data = _PreviewVO()
        data.title = BWPersonality.g_lobbyInterview[0]
        data.question = BWPersonality.g_lobbyInterview[1]
        arenaData = db.DBLogic.g_instance.getArenaData(BWPersonality.g_lastMapID)
        data.arenaIcoPath = arenaData.hudIcoPath
        BWPersonality.g_lobbyInterview = [None, None]
        GUIWindowAccount.initialized(self, data)
        GlobalEvents.onScreenshot += self.__onScreenshot
        return

    def dispossessUI(self):
        LOG_INFO('dispossess Interview')
        GlobalEvents.onScreenshot -= self.__onScreenshot
        GUIWindowAccount.dispossessUI(self)
        self.removeAllCallbacks()

    def onAnswer(self, data):
        LOG_NOTE('Interview:onAnswer', data)
        import BWPersonality
        BWPersonality.g_lobbyInterview[0] = None
        player = BigWorld.player()
        from Account import PlayerAccount
        if player != None:
            if player.__class__ == PlayerAccount:
                player.accountCmd.interviewAnswer(data)
            BigWorld.callback(0.0, player.receivePlayerInfoPostProcess)
        return

    def __onScreenshot(self, path):
        self.call_1('interview.screenshot', localizeMessages('LOBBY_MSG_SCREENSHOT').format(adress=path))