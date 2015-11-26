# Embedded file name: scripts/client/tutorial/gui/Scaleform/quests/pop_ups.py
from gui.Scaleform.daapi.view.lobby.AwardWindow import AwardWindow
from gui.server_events.awards import FormattedAward
from gui.server_events.bonuses import getTutorialBonusObj
from helpers import i18n
from tutorial.control import TutorialProxyHolder
from tutorial.data.events import ClickEvent
from tutorial.gui import GUI_EFFECT_NAME
from tutorial.logger import LOG_ERROR

class TutorialQuestAwardWindow(AwardWindow, TutorialProxyHolder):

    def __init__(self, content):
        ctx = {'award': _TutorialQuestAward(content)}
        self._content = content
        super(TutorialQuestAwardWindow, self).__init__(ctx)

    def onWindowClose(self):
        self._onMouseClicked('closeID')
        self._stop()

    def onTakeNextClick(self):
        self._onMouseClicked('nextID')
        self._stop()

    def _stop(self):
        self._content.clear()
        self._gui.effects.stop(GUI_EFFECT_NAME.SHOW_WINDOW, effectID=self.uniqueName)

    def _onMouseClicked(self, targetKey):
        if targetKey in self._content:
            targetID = self._content[targetKey]
            if len(targetID):
                self._gui.onGUIInput(ClickEvent(targetID))
            else:
                LOG_ERROR('ID of target is empty', targetKey)
        else:
            LOG_ERROR('Target not found in data', targetKey)


class _TutorialQuestAward(FormattedAward):

    def __init__(self, content):
        super(_TutorialQuestAward, self).__init__()
        self.__content = content

    def clear(self):
        super(_TutorialQuestAward, self).clear()
        self.__content = None
        return

    def getButtonStates(self):
        return (False, True, self.__content['showQuestsBtn'])

    def getWindowTitle(self):
        return i18n.makeString('#tutorial:tutorialQuest/awardWindow/title')

    def getBackgroundImage(self):
        return self.__content['bgImage']

    def getHeader(self):
        return i18n.makeString(self.__content['header'])

    def getDescription(self):
        return i18n.makeString(self.__content['description'])

    def getBodyButtonText(self):
        return i18n.makeString('#tutorial:tutorialQuest/awardWindow/nextQuest')

    def _getBonuses(self):
        bonuses = self.__content.get('bonuses', {})
        result = []
        for n, v in bonuses.iteritems():
            result.append(getTutorialBonusObj(n, v))

        return result