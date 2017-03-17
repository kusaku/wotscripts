# Embedded file name: scripts/client/eventhandlers/questEvents.py
import BWPersonality
from gui.WindowsManager import g_windowsManager
from debug_utils import LOG_DEBUG, LOG_NOTE, LOG_INFO
import BigWorld
from consts import EMPTY_IDTYPELIST
import GlobalEvents
from gui.hud import BattleQuest, SelectedComplexQuest
from Helpers.i18n import localizeLobby, localizeAchievementsInQuest

def onQuestSelectConsist(event):
    LOG_DEBUG('Select quest info: ', format(event.ob))
    questID = event.ob.get('questID')
    BWPersonality.g_questSelected = SelectedComplexQuest(questID)
    if questID:
        accountUI = g_windowsManager.getAccountUI()
        if accountUI:
            BWPersonality.g_questSelected.quests[questID] = BattleQuest(questID)
            accountUI.viewIFace([[{'IQuestDescription': {}}, [[questID, 'battlequest']]]])
            accountUI.viewIFace([[{'IQuestResults': {}}, [[questID, 'battlequest']]]])
    else:
        GlobalEvents.onQuestSelectUpdated()


def onQuestDescription(event):
    questID = event.idTypeList[0][0]
    LOG_DEBUG('Quest description: ', questID, format(event.ob))
    name = event.ob.get('name')
    description = event.ob.get('description')
    consistMain = event.ob.get('consistMain')
    consistChildes = event.ob.get('consistChildes')
    questSelected = BWPersonality.g_questSelected
    if questSelected and questSelected.mainQuestId == consistMain:
        quest = questSelected.quests.get(questID)
        if quest:
            if description and description.isupper():
                description = localizeLobby(description)
            quest.desc = localizeAchievementsInQuest(description)
            quest.name = name
            quest.isMain = questID == consistMain
            accountUI = g_windowsManager.getAccountUI()
            if accountUI:
                for chQuestId in consistChildes:
                    questSelected.quests[chQuestId] = BattleQuest(chQuestId)
                    accountUI.viewIFace([[{'IQuestDescription': {}}, [[chQuestId, 'battlequest']]]])
                    accountUI.viewIFace([[{'IQuestResults': {}}, [[chQuestId, 'battlequest']]]])

            if questSelected.isDataFull():
                GlobalEvents.onQuestSelectUpdated()


def onQuestResults(event):
    questID = event.idTypeList[0][0]
    LOG_DEBUG('Quest Results: ', questID, format(event.ob))
    questSelected = BWPersonality.g_questSelected
    if questSelected:
        quest = questSelected.quests.get(questID)
        if quest:
            quest.isComplete = False
            progress = event.ob.get('progress', [])
            if len(progress) > 0:
                quest.isComplete = progress[0].get('count', 0) > 0
            if questSelected.isDataFull():
                GlobalEvents.onQuestSelectUpdated()